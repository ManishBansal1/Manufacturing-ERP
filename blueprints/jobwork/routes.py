from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)
from flask_login import login_required
from datetime import date

from models import (
    db,
    VendorMaster,
    JobWorkHeader,
    JobWorkDetail,
    JobWorkLedger,
    JobWorkReceipt,
    JobWorkReceiptDetail,
    ItemMaster,
    RecipeHeader,
    RecipeInput,
    RecipeByProduct,
    InventoryLedger,
    LocationMaster

)

from services.inventory_costing import update_inventory_cost

from . import jobwork_bp


@jobwork_bp.route("/jobwork")
@login_required
def jobwork_list():

    jobs = JobWorkHeader.query.order_by(
        JobWorkHeader.id.desc()
    ).all()

    return render_template(
        "jobwork/jobwork_list.html",
        jobs=jobs
    )

@jobwork_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_jobwork():

    vendors = VendorMaster.query.order_by(
        VendorMaster.vendor_name
    ).all()

    items = ItemMaster.query.order_by(
    ItemMaster.item_name
    ).all()

    locations = LocationMaster.query.order_by(
        LocationMaster.location_name
    ).all()

    if request.method == "POST":

        existing = JobWorkHeader.query.filter_by(
            jobwork_no=request.form["jobwork_no"].strip()
        ).first()

        if existing:

            flash(
                "Job Work Number already exists.",
                "danger"
            )

            return render_template(

                "jobwork/add_jobwork.html",

                vendors=vendors,

                items=items,

                locations=locations

            )

        job = JobWorkHeader(

            jobwork_no=request.form["jobwork_no"],

            jobwork_date=date.fromisoformat(
                request.form["jobwork_date"]
            ),

            vendor_id=request.form["vendor_id"],

            location_id=request.form["location_id"],

            output_item_id=request.form["output_item_id"],

            planned_output_qty=float(request.form["planned_output_qty"]),

            expected_return_date=(
                date.fromisoformat(
                    request.form["expected_return_date"]
                )
                if request.form["expected_return_date"]
                else None
            ),

            status="Open",

            remarks=request.form["remarks"]

        )

        db.session.add(job)
        db.session.commit()

        

        return redirect(
            url_for(
                "jobwork.jobwork_details",
                id=job.id
            )
        )

    return render_template(

        "jobwork/add_jobwork.html",

        vendors=vendors,

        items=items,

        locations=locations

    )

@jobwork_bp.route("/details/<int:id>", methods=["GET","POST"])
@login_required
def jobwork_details(id):

    job = JobWorkHeader.query.get_or_404(id)

    
    details = JobWorkDetail.query.filter_by(
        job_work_id=id
    ).all()


    

    if len(details) == 0:

        recipe = RecipeHeader.query.filter_by(
            output_item_id=job.output_item_id,
            active=True
        ).first()

        if recipe:

            factor = job.planned_output_qty / recipe.output_qty

            # -------------------------
            # INPUT MATERIALS
            # -------------------------

            for row in recipe.inputs:

                db.session.add(

                    JobWorkDetail(

                        job_work_id=job.id,

                        item_id=row.input_item_id,

                        line_type="INPUT",

                        expected_qty=row.input_qty * factor,

                        actual_qty=0,

                        remarks=""

                    )

                )

            # -------------------------
            # SCRAP
            # -------------------------

            for row in recipe.byproducts:

                db.session.add(

                    JobWorkDetail(

                        job_work_id=job.id,

                        item_id=row.byproduct_item_id,

                        line_type="SCRAP",

                        expected_qty=row.byproduct_qty * factor,

                        actual_qty=0,

                        remarks=""

                    )

                )

            db.session.commit()

            details = JobWorkDetail.query.filter_by(
            job_work_id=id
            ).all()



    if request.method == "POST":

    

        job.job_work_cost = float(
                    request.form["job_work_cost"]
                )

        for row in details:

            qty = request.form.get(
                        f"expected_qty_{row.id}"
                    )

            if qty:

                        row.expected_qty = float(qty)

            # Also update item_id in case changed
            item_id = request.form.get(
                f"item_id_{row.id}"
            )
            if item_id:
                row.item_id = int(item_id)

        db.session.commit()

        flash(
                    f"Job Work Order {job.jobwork_no} saved successfully.",
                    "success"
                )
        

        
        return redirect(
                    url_for(
                        "jobwork.jobwork_list"
                        #id=id
                    )
                )
    

    items = ItemMaster.query.order_by(
        ItemMaster.item_name
    ).all()

    return render_template(

        "jobwork/jobwork_details.html",

        job=job,

        details=details,

        items=items

    )

@jobwork_bp.route("/issue/<int:id>", methods=["POST"])
@login_required
def issue_jobwork(id):
    """
    Issue materials to job worker:
    1. Reduce inventory from main stock (InventoryLedger qty_out)
    2. Create JobWorkLedger entries (tracking what's at vendor)
    """
    job = JobWorkHeader.query.get_or_404(id)

    if job.status not in ["Open", "Issued"]:
        flash("Cannot issue materials for this job work status.", "danger")
        return redirect(url_for("jobwork.jobwork_list"))

    details = JobWorkDetail.query.filter_by(
        job_work_id=id,
        line_type="INPUT"
    ).all()

    for row in details:
        issue_qty = row.expected_qty

        if issue_qty <= 0:
            continue

        last_ledger = (
            InventoryLedger.query
            .filter_by(
                item_id=row.item_id,
                location_id=job.location_id
            )
            .order_by(
                InventoryLedger.id.desc()
            )
            .first()
        )

        avg_rate = last_ledger.weighted_average_rate if last_ledger else 0
        issue_value = issue_qty * avg_rate

        # 1. REDUCE MAIN INVENTORY (qty_out)
        ledger_out = InventoryLedger(
            trans_date=date.today(),
            item_id=row.item_id,
            location_id=job.location_id,
            qty_out=issue_qty,
            unit_cost=avg_rate,
            value_out=issue_value,
            reference_type="JOB_WORK_ISSUE",
            reference_id=job.id,
            remarks=f"Issued to Job Work {job.jobwork_no}"
        )
        db.session.add(ledger_out)

        # 2. CREATE/UPDATE JOB WORK LEDGER
        jw_ledger = JobWorkLedger.query.filter_by(
            job_work_id=job.id,
            item_id=row.item_id,
            line_type="INPUT"
        ).first()

        if jw_ledger:
            jw_ledger.issued_qty += issue_qty
            jw_ledger.balance_qty = jw_ledger.issued_qty - jw_ledger.received_qty
            jw_ledger.issued_value = jw_ledger.issued_qty * avg_rate
        else:
            jw_ledger = JobWorkLedger(
                job_work_id=job.id,
                item_id=row.item_id,
                line_type="INPUT",
                issued_qty=issue_qty,
                received_qty=0,
                balance_qty=issue_qty,
                issued_rate=avg_rate,
                issued_value=issue_value
            )
            db.session.add(jw_ledger)

        update_inventory_cost(row.item_id)

    # Also issue SCRAP items
    scrap_details = JobWorkDetail.query.filter_by(
        job_work_id=id,
        line_type="SCRAP"
    ).all()

    for row in scrap_details:
        issue_qty = row.expected_qty
        if issue_qty <= 0:
            continue

        last_ledger = (
            InventoryLedger.query
            .filter_by(
                item_id=row.item_id,
                location_id=job.location_id
            )
            .order_by(InventoryLedger.id.desc())
            .first()
        )

        avg_rate = last_ledger.weighted_average_rate if last_ledger else 0
        issue_value = issue_qty * avg_rate

        ledger_out = InventoryLedger(
            trans_date=date.today(),
            item_id=row.item_id,
            location_id=job.location_id,
            qty_out=issue_qty,
            unit_cost=avg_rate,
            value_out=issue_value,
            reference_type="JOB_WORK_ISSUE",
            reference_id=job.id,
            remarks=f"Scrap issued to Job Work {job.jobwork_no}"
        )
        db.session.add(ledger_out)

        jw_ledger = JobWorkLedger.query.filter_by(
            job_work_id=job.id,
            item_id=row.item_id,
            line_type="SCRAP"
        ).first()

        if jw_ledger:
            jw_ledger.issued_qty += issue_qty
            jw_ledger.balance_qty = jw_ledger.issued_qty - jw_ledger.received_qty
        else:
            jw_ledger = JobWorkLedger(
                job_work_id=job.id,
                item_id=row.item_id,
                line_type="SCRAP",
                issued_qty=issue_qty,
                received_qty=0,
                balance_qty=issue_qty,
                issued_rate=avg_rate,
                issued_value=issue_value
            )
            db.session.add(jw_ledger)

        update_inventory_cost(row.item_id)

    job.status = "Issued"
    db.session.commit()

    flash(
        f"Materials issued for Job Work {job.jobwork_no}. Inventory updated.",
        "success"
    )

    return redirect(url_for("jobwork.jobwork_list"))


@jobwork_bp.route("/receive/<int:id>", methods=["GET", "POST"])
@login_required
def receive_jobwork(id):
    """
    Receive finished goods from job worker:
    1. Reduce from JobWorkLedger (what was at vendor)
    2. Add output item + scrap back to main inventory
    3. Add job work cost to inventory value
    """
    job = JobWorkHeader.query.get_or_404(id)

    if job.status not in ["Issued", "Partially Received"]:
        flash("Cannot receive - Job Work not issued yet.", "danger")
        return redirect(url_for("jobwork.jobwork_list"))

    locations = LocationMaster.query.order_by(
        LocationMaster.location_name
    ).all()

    # Calculate already received quantity
    already_received = db.session.query(
        db.func.coalesce(db.func.sum(JobWorkReceipt.output_qty_received), 0)
    ).filter_by(job_work_id=job.id).scalar() or 0

    balance_to_receive = job.planned_output_qty - already_received

    if request.method == "POST":
        receipt = JobWorkReceipt(
            receipt_no=request.form["receipt_no"],
            receipt_date=date.fromisoformat(request.form["receipt_date"]),
            job_work_id=job.id,
            location_id=request.form["location_id"],
            output_qty_received=float(request.form.get("output_qty_received", 0)),
            output_qty_rejected=float(request.form.get("output_qty_rejected", 0)),
            scrap_qty_received=float(request.form.get("scrap_qty_received", 0)),
            job_work_cost=float(request.form.get("job_work_cost", job.job_work_cost or 0)),
            remarks=request.form.get("remarks", "")
        )
        db.session.add(receipt)
        db.session.flush()

        output_received = receipt.output_qty_received
        job_cost_per_unit = receipt.job_work_cost
        total_job_cost = output_received * job_cost_per_unit
        receipt.total_cost = total_job_cost

        # 1. RECEIVE OUTPUT ITEM BACK TO MAIN INVENTORY
        if output_received > 0:
            # Calculate material cost proportionally from issued items
            material_cost = 0
            jw_ledgers = JobWorkLedger.query.filter_by(
                job_work_id=job.id,
                line_type="INPUT"
            ).all()

            total_issued_value = sum(jwl.issued_value for jwl in jw_ledgers)
            total_issued_qty = sum(jwl.issued_qty for jwl in jw_ledgers)

            if total_issued_qty > 0:
                # Proportionate material cost based on received vs planned
                receive_ratio = output_received / job.planned_output_qty
                material_cost = total_issued_value * receive_ratio

            total_output_value = material_cost + total_job_cost
            unit_cost = total_output_value / output_received if output_received > 0 else 0

            # Add to main inventory - ONLY ONE ENTRY
            ledger_in = InventoryLedger(
                trans_date=receipt.receipt_date,
                item_id=job.output_item_id,
                location_id=receipt.location_id,
                qty_in=output_received,
                unit_cost=unit_cost,
                value_in=total_output_value,
                reference_type="JOB_WORK_RECEIPT",
                reference_id=receipt.id,
                remarks=f"Received from Job Work {job.jobwork_no}"
            )
            db.session.add(ledger_in)

            update_inventory_cost(job.output_item_id)

        # 2. RECEIVE SCRAP BACK TO MAIN INVENTORY
        scrap_received = receipt.scrap_qty_received
        if scrap_received > 0:
            scrap_details = JobWorkDetail.query.filter_by(
                job_work_id=job.id,
                line_type="SCRAP"
            ).all()

            for scrap in scrap_details:
                ledger_scrap = InventoryLedger(
                    trans_date=receipt.receipt_date,
                    item_id=scrap.item_id,
                    location_id=receipt.location_id,
                    qty_in=scrap_received,
                    unit_cost=0,
                    value_in=0,
                    reference_type="JOB_WORK_RECEIPT",
                    reference_id=receipt.id,
                    remarks=f"Scrap received from Job Work {job.jobwork_no}"
                )
                db.session.add(ledger_scrap)
                update_inventory_cost(scrap.item_id)

        # 3. UPDATE JOB WORK LEDGER (reduce balances proportionally)
        receive_ratio = output_received / job.planned_output_qty if job.planned_output_qty > 0 else 0

        for jwl in JobWorkLedger.query.filter_by(job_work_id=job.id).all():
            qty_to_receive = jwl.issued_qty * receive_ratio
            jwl.received_qty += qty_to_receive
            jwl.balance_qty = jwl.issued_qty - jwl.received_qty

        # 4. SAVE RECEIPT DETAILS for each input line
        for detail in JobWorkDetail.query.filter_by(job_work_id=job.id).all():
            received = 0
            rejected = 0

            if detail.line_type == "INPUT":
                received = float(request.form.get(f"received_qty_{detail.id}", 0))
                rejected = float(request.form.get(f"rejected_qty_{detail.id}", 0))

            receipt_detail = JobWorkReceiptDetail(
                job_work_receipt_id=receipt.id,
                job_work_detail_id=detail.id,
                item_id=detail.item_id,
                line_type=detail.line_type,
                issued_qty=detail.expected_qty,
                received_qty=received,
                rejected_qty=rejected,
                rate=detail.rate,
                value=detail.value
            )
            db.session.add(receipt_detail)

        # Update job status
        total_received_now = already_received + output_received

        if total_received_now >= job.planned_output_qty:
            job.status = "Received"
        else:
            job.status = "Partially Received"

        db.session.commit()

        flash(
            f"Job Work {job.jobwork_no} received successfully. "
            f"Received: {output_received}, Balance: {job.planned_output_qty - total_received_now}",
            "success"
        )

        return redirect(url_for("jobwork.jobwork_list"))

    # GET request - show receive form
    jw_ledger = JobWorkLedger.query.filter_by(
        job_work_id=job.id
    ).all()

    return render_template(
        "jobwork/receive_jobwork.html",
        job=job,
        locations=locations,
        jw_ledger=jw_ledger,
        already_received=already_received,
        balance_to_receive=balance_to_receive,
        today=date.today().isoformat()
    )


@jobwork_bp.route("/view/<int:id>")
@login_required
def view_jobwork(id):
    job = JobWorkHeader.query.get_or_404(id)

    # Calculate totals
    already_received = db.session.query(
        db.func.coalesce(db.func.sum(JobWorkReceipt.output_qty_received), 0)
    ).filter_by(job_work_id=job.id).scalar() or 0

    balance_to_receive = job.planned_output_qty - already_received

    return render_template(
        "jobwork/view_jobwork.html",
        job=job,
        already_received=already_received,
        balance_to_receive=balance_to_receive
    )


@jobwork_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_jobwork(id):
    """
    Delete job work only if no receipts have been made.
    If materials were issued, reverse inventory before deleting.
    """
    job = JobWorkHeader.query.get_or_404(id)

    # Check if any receipts exist
    receipt_count = JobWorkReceipt.query.filter_by(job_work_id=job.id).count()

    if receipt_count > 0:
        flash(
            "Cannot delete - receipts already exist for this job work.",
            "danger"
        )
        return redirect(url_for("jobwork.jobwork_list"))

    # Check if materials were issued (JobWorkLedger exists)
    jw_ledgers = JobWorkLedger.query.filter_by(job_work_id=job.id).all()

    if jw_ledgers:
        # Materials were issued - reverse inventory
        for jwl in jw_ledgers:
            if jwl.issued_qty > 0:
                # Add back to main inventory
                ledger_in = InventoryLedger(
                    trans_date=date.today(),
                    item_id=jwl.item_id,
                    location_id=job.location_id,
                    qty_in=jwl.issued_qty,
                    unit_cost=jwl.issued_rate,
                    value_in=jwl.issued_value,
                    reference_type="JOB_WORK_CANCEL",
                    reference_id=job.id,
                    remarks=f"Reversed - Job Work {job.jobwork_no} deleted"
                )
                db.session.add(ledger_in)
                update_inventory_cost(jwl.item_id)

    # Manually delete child records first to avoid cascade issues
    JobWorkLedger.query.filter_by(job_work_id=job.id).delete()
    JobWorkDetail.query.filter_by(job_work_id=job.id).delete()

    # Now delete the header
    db.session.delete(job)
    db.session.commit()

    flash(
        f"Job Work {job.jobwork_no} deleted." + 
        (" Inventory reversed." if jw_ledgers else ""),
        "success"
    )

    return redirect(url_for("jobwork.jobwork_list"))


@jobwork_bp.route("/ledger")
@login_required
def jobwork_ledger():
    """
    View all job work inventory - what's issued to vendors
    """
    ledger = JobWorkLedger.query.join(
        JobWorkHeader
    ).join(
        ItemMaster
    ).filter(
        JobWorkLedger.balance_qty > 0
    ).order_by(
        JobWorkLedger.id.desc()
    ).all()

    return render_template(
        "jobwork/jobwork_ledger.html",
        ledger=ledger
    )