from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from flask_login import login_required
from datetime import date

from models import (
    db,
    VendorMaster,
    JobWorkHeader,
    JobWorkDetail,
    ItemMaster,
    RecipeHeader,
    RecipeInput,
    RecipeByProduct

)

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

                items=items

            )

        job = JobWorkHeader(

            jobwork_no=request.form["jobwork_no"],

            jobwork_date=date.fromisoformat(
                request.form["jobwork_date"]
            ),

            vendor_id=request.form["vendor_id"],

            output_item_id=request.form["output_item_id"],

            planned_output_qty=request.form["planned_output_qty"],

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

        items=items

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

        db.session.commit()

        flash(
                    f"Job Work Order {job.jobwork_no} saved successfully.",
                    "success"
                )
        

        
        return redirect(
                    url_for(
                        "jobwork.jobwork_list",
                        id=id
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