from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, jsonify
)
from flask_login import login_required, current_user
from datetime import date, datetime, time, timedelta
from decimal import Decimal

from models import (
    db, LabourTypeMaster, LabourContractorMaster, LabourMaster,
    LabourDailySheetHeader, LabourDailySheetEntry, LabourDailySheetEntryDetail,
    ItemMaster, LocationMaster, RecipeHeader, InventoryLedger
)

from services.inventory_costing import update_inventory_cost

#labour_bp = Blueprint("labour", __name__, url_prefix="/labour")
from . import labour_bp

# ============================================================
# LABOUR TYPE MASTER
# ============================================================

@labour_bp.route("/types")
@login_required
def labour_types():

    labour_types = LabourTypeMaster.query.order_by(
        LabourTypeMaster.type_name
    ).all()

    return render_template(
        "labour/labour_types.html",
        labour_types=labour_types
    )


@labour_bp.route("/types/add", methods=["GET", "POST"])
@login_required
def add_labour_type():
    if request.method == "POST":
        labour_type = LabourTypeMaster(
            type_code=request.form["type_code"].strip(),
            type_name=request.form["type_name"].strip(),
            description=request.form.get("description", "")
        )
        db.session.add(labour_type)
        db.session.commit()
        flash("Labour Type added successfully.", "success")
        return redirect(url_for("labour.labour_types"))
    return render_template("labour/add_labour_type.html")


@labour_bp.route("/types/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_labour_type(id):
    labour_type = LabourTypeMaster.query.get_or_404(id)
    if request.method == "POST":
        labour_type.type_code = request.form["type_code"].strip()
        labour_type.type_name = request.form["type_name"].strip()
        labour_type.description = request.form.get("description", "")
        labour_type.active = "active" in request.form
        db.session.commit()
        flash("Labour Type updated.", "success")
        return redirect(url_for("labour.labour_types"))
    return render_template("labour/edit_labour_type.html", labour_type=labour_type)

@labour_bp.route("/types/view/<int:id>")
@login_required
def view_labour_type(id):

    labour_type = LabourTypeMaster.query.get_or_404(id)

    return render_template(
        "labour/view_labour_type.html",
        labour_type=labour_type
    )


# ============================================================
# LABOUR CONTRACTOR MASTER
# ============================================================

@labour_bp.route("/contractors")
@login_required
def labour_contractors():
    contractors = LabourContractorMaster.query.order_by(
        LabourContractorMaster.contractor_name
    ).all()
    return render_template("labour/labour_contractors.html", contractors=contractors)


@labour_bp.route("/contractors/add", methods=["GET", "POST"])
@login_required
def add_labour_contractor():
    if request.method == "POST":
        contractor = LabourContractorMaster(
            contractor_code=request.form["contractor_code"],
            contractor_name=request.form["contractor_name"].strip(),
            contact_person=request.form.get("contact_person", ""),
            mobile=request.form.get("mobile", ""),
            email=request.form.get("email", ""),
            gst_no=request.form.get("gst_no", ""),
            pan_no=request.form.get("pan_no", ""),
            address=request.form.get("address", ""),
            city=request.form.get("city", ""),
            state=request.form.get("state", ""),
            active="active" in request.form
        )
        db.session.add(contractor)
        db.session.commit()
        flash("Labour Contractor added successfully.", "success")
        return redirect(url_for("labour.labour_contractors"))
    return render_template("labour/add_labour_contractor.html")


@labour_bp.route("/contractors/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_labour_contractor(id):
    contractor = LabourContractorMaster.query.get_or_404(id)
    if request.method == "POST":
        contractor.contractor_code=request.form["contractor_code"]
        contractor.contractor_name=request.form["contractor_name"]
        contractor.contact_person=request.form["contact_person"]
        contractor.mobile=request.form["mobile"]
        contractor.email=request.form["email"]
        contractor.gst_no=request.form["gst_no"]
        contractor.pan_no=request.form["pan_no"]
        contractor.address=request.form["address"]
        contractor.city=request.form["city"]
        contractor.state=request.form["state"]
        contractor.active="active" in request.form
        db.session.commit()
        flash("Labour Contractor updated.", "success")
        return redirect(url_for("labour.labour_contractors"))
    return render_template("labour/edit_labour_contractor.html", contractor=contractor)


@labour_bp.route("/contractors/view/<int:id>")
@login_required
def view_labour_contractor(id):

    contractor = LabourContractorMaster.query.get_or_404(id)

    return render_template(
        "labour/view_labour_contractor.html",
        contractor=contractor
    )

# ============================================================
# LABOUR MASTER
# ============================================================

@labour_bp.route("/master")
@login_required
def labour_master_list():
    labours = LabourMaster.query.order_by(LabourMaster.labour_name).all()
    return render_template("labour/labour_master_list.html", labours=labours)


@labour_bp.route("/master/add", methods=["GET", "POST"])
@login_required
def add_labour():
    types = LabourTypeMaster.query.filter_by(active=True).order_by(
        LabourTypeMaster.type_name
    ).all()
    contractors = LabourContractorMaster.query.filter_by(active=True).order_by(
        LabourContractorMaster.contractor_name
    ).all()
    locations = LocationMaster.query.filter_by(active=True).order_by(
        LocationMaster.location_name
    ).all()

    if request.method == "POST":
        # Calculate age from DOB
        dob = None
        age = None
        if request.form.get("date_of_birth"):
            dob = date.fromisoformat(request.form["date_of_birth"])
            age = (date.today() - dob).days // 365

        labour = LabourMaster(
            labour_name=request.form["labour_name"].strip(),
            father_name=request.form.get("father_name", ""),
            gender=request.form.get("gender", ""),
            date_of_birth=dob,
            age=age,
            blood_group=request.form.get("blood_group", ""),
            aadhar_no=request.form.get("aadhar_no", ""),
            mobile=request.form.get("mobile", ""),
            address=request.form.get("address", ""),
            city=request.form.get("city", ""),
            state=request.form.get("state", ""),
            pincode=request.form.get("pincode", ""),
            labour_type_id=request.form["labour_type_id"],
            contractor_id=request.form["contractor_id"],
            #location_id=request.form["location_id"],
            #wage_type=request.form["wage_type"],
            daily_wage_rate=float(request.form.get("daily_wage_rate", 0)),
            contractor_rate=float(request.form.get("contractor_rate", 0)),
            active="active" in request.form
        )
        db.session.add(labour)
        db.session.flush()
        labour.labour_code = f"LB{labour.id:05d}"
        db.session.commit()
        flash("Labour registered successfully.", "success")
        return redirect(url_for("labour.labour_master_list"))

    return render_template(
        "labour/add_labour.html",
        types=types,
        contractors=contractors,
        locations=locations
    )


@labour_bp.route("/master/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_labour(id):
    labour = LabourMaster.query.get_or_404(id)
    types = LabourTypeMaster.query.filter_by(active=True).order_by(
        LabourTypeMaster.type_name
    ).all()
    contractors = LabourContractorMaster.query.filter_by(active=True).order_by(
        LabourContractorMaster.contractor_name
    ).all()
    locations = LocationMaster.query.filter_by(active=True).order_by(
        LocationMaster.location_name
    ).all()

    if request.method == "POST":
        dob = None
        age = None
        if request.form.get("date_of_birth"):
            dob = date.fromisoformat(request.form["date_of_birth"])
            age = (date.today() - dob).days // 365

        labour.labour_name = request.form["labour_name"].strip()
        labour.father_name = request.form.get("father_name", "")
        labour.gender = request.form.get("gender", "")
        labour.date_of_birth = dob
        labour.age = age
        labour.blood_group = request.form.get("blood_group", "")
        labour.aadhar_no = request.form.get("aadhar_no", "")
        labour.mobile = request.form.get("mobile", "")
        labour.address = request.form.get("address", "")
        labour.city = request.form.get("city", "")
        labour.state = request.form.get("state", "")
        labour.pincode = request.form.get("pincode", "")
        labour.labour_type_id = request.form["labour_type_id"]
        labour.contractor_id = request.form["contractor_id"]
        labour.location_id = request.form["location_id"]
        labour.wage_type = request.form["wage_type"]
        labour.daily_wage_rate = float(request.form.get("daily_wage_rate", 0))
        labour.contractor_rate = float(request.form.get("contractor_rate", 0))
        labour.active = "active" in request.form
        db.session.commit()
        flash("Labour updated successfully.", "success")
        return redirect(url_for("labour.labour_master_list"))

    return render_template(
        "labour/edit_labour.html",
        labour=labour,
        types=types,
        contractors=contractors,
        locations=locations
    )


@labour_bp.route("/master/view/<int:id>")
@login_required
def view_labour(id):
    labour = LabourMaster.query.get_or_404(id)
    return render_template("labour/view_labour.html", labour=labour)


# ============================================================
# DAILY SHEET
# ============================================================

@labour_bp.route("/daily-sheet")
@login_required
def daily_sheet_list():
    sheets = LabourDailySheetHeader.query.order_by(
        LabourDailySheetHeader.sheet_date.desc()
    ).all()
    return render_template("labour/daily_sheet_list.html", sheets=sheets)


@labour_bp.route("/daily-sheet/add", methods=["GET", "POST"])
@login_required
def add_daily_sheet():
    contractors = LabourContractorMaster.query.filter_by(active=True).order_by(
        LabourContractorMaster.contractor_name
    ).all()
    locations = LocationMaster.query.filter_by(active=True).order_by(
        LocationMaster.location_name
    ).all()

    if request.method == "POST":
        sheet = LabourDailySheetHeader(
            sheet_no=request.form["sheet_no"].strip(),
            sheet_date=date.fromisoformat(request.form["sheet_date"]),
            contractor_id=request.form["contractor_id"],
            location_id=request.form["location_id"],
            remarks=request.form.get("remarks", ""),
            status="DRAFT"
        )
        db.session.add(sheet)
        db.session.commit()
        flash("Daily Sheet created. Now add labour entries.", "success")
        return redirect(url_for("labour.daily_sheet_entries", sheet_id=sheet.id))

    # Auto-generate sheet number
    last_sheet = LabourDailySheetHeader.query.order_by(
        LabourDailySheetHeader.id.desc()
    ).first()
    next_no = (last_sheet.id + 1) if last_sheet else 1
    sheet_no = f"LS-{date.today().strftime('%Y%m%d')}-{next_no:04d}"

    return render_template(
        "labour/add_daily_sheet.html",
        contractors=contractors,
        locations=locations,
        sheet_no=sheet_no,
        today=date.today().isoformat()
    )


@labour_bp.route("/daily-sheet/<int:sheet_id>/entries", methods=["GET", "POST"])
@login_required
def daily_sheet_entries(sheet_id):
    sheet = LabourDailySheetHeader.query.get_or_404(sheet_id)
    labours = LabourMaster.query.filter_by(
        contractor_id=sheet.contractor_id,
        active=True
    ).order_by(LabourMaster.labour_name).all()
    items = ItemMaster.query.filter(
        ItemMaster.item_type.in_(["Intermediate Material", "Assembled Goods", "Finished Goods"])
    ).order_by(ItemMaster.item_name).all()
    recipes = RecipeHeader.query.filter_by(active=True).order_by(RecipeHeader.recipe_name).all()

    if request.method == "POST":
        # Save all entries from form
        labour_ids = request.form.getlist("labour_id")
        time_ins = request.form.getlist("time_in")
        time_outs = request.form.getlist("time_out")
        break_hours = request.form.getlist("break_hours")

        for i, labour_id in enumerate(labour_ids):
            if not labour_id:
                continue

            labour = LabourMaster.query.get(int(labour_id))

            # Calculate total hours
            t_in = datetime.strptime(time_ins[i], "%H:%M").time()
            t_out = datetime.strptime(time_outs[i], "%H:%M").time()
            break_h = float(break_hours[i] or 0)

            # Convert to datetime for calculation
            dt_in = datetime.combine(date.today(), t_in)
            dt_out = datetime.combine(date.today(), t_out)
            if dt_out < dt_in:
                dt_out += timedelta(days=1)

            total_hours = (dt_out - dt_in).total_seconds() / 3600 - break_h

            # Calculate wages
            if labour.wage_type == "DAILY":
                # Daily wage = (daily_rate / standard_hours) * actual_hours
                # Standard day = 8 hours
                standard_hours = 8
                daily_rate = labour.daily_wage_rate
                total_wages = (daily_rate / standard_hours) * total_hours if total_hours > 0 else 0
                wage_type = "DAILY"
            else:
                # Piece rate - will be calculated per item
                total_wages = 0
                wage_type = "PIECE"

            entry = LabourDailySheetEntry(
                sheet_id=sheet.id,
                labour_id=labour.id,
                labour_type_id=labour.labour_type_id,
                time_in=t_in,
                time_out=t_out,
                break_hours=break_h,
                total_hours=round(total_hours, 2),
                wage_type=wage_type,
                daily_rate=labour.daily_wage_rate if labour.wage_type == "DAILY" else 0,
                total_wages=round(total_wages, 2)
            )
            db.session.add(entry)
            db.session.flush()

            # Save item details for this labour
            item_ids = request.form.getlist(f"item_id_{labour_id}")
            start_times = request.form.getlist(f"start_time_{labour_id}")
            end_times = request.form.getlist(f"end_time_{labour_id}")
            qty_produced = request.form.getlist(f"qty_produced_{labour_id}")
            recipe_ids = request.form.getlist(f"recipe_id_{labour_id}")

            for j, item_id in enumerate(item_ids):
                if not item_id:
                    continue

                item = ItemMaster.query.get(int(item_id))

                s_time = datetime.strptime(start_times[j], "%H:%M").time()
                e_time = datetime.strptime(end_times[j], "%H:%M").time()

                dt_s = datetime.combine(date.today(), s_time)
                dt_e = datetime.combine(date.today(), e_time)
                if dt_e < dt_s:
                    dt_e += timedelta(days=1)
                hours = (dt_e - dt_s).total_seconds() / 3600

                # Calculate wages for this item
                if wage_type == "PIECE":
                    piece_rate = item.piece_rate or 0
                    piece_wages = float(qty_produced[j] or 0) * piece_rate
                    prop_wages = 0
                else:
                    # Daily wage - proportionate
                    if total_hours > 0:
                        prop_wages = (total_wages / total_hours) * hours
                    else:
                        prop_wages = 0
                    piece_rate = 0
                    piece_wages = 0

                detail = LabourDailySheetEntryDetail(
                    entry_id=entry.id,
                    item_id=int(item_id),
                    recipe_id=int(recipe_ids[j]) if recipe_ids[j] else None,
                    start_time=s_time,
                    end_time=e_time,
                    hours_worked=round(hours, 2),
                    qty_produced=float(qty_produced[j] or 0),
                    piece_rate=piece_rate,
                    piece_wages=round(piece_wages, 2),
                    proportionate_wages=round(prop_wages, 2)
                )
                db.session.add(detail)

        db.session.commit()
        flash("Labour entries saved successfully.", "success")
        return redirect(url_for("labour.daily_sheet_list"))

    return render_template(
        "labour/daily_sheet_entries.html",
        sheet=sheet,
        labours=labours,
        items=items,
        recipes=recipes
    )


@labour_bp.route("/daily-sheet/<int:sheet_id>/view")
@login_required
def view_daily_sheet(sheet_id):
    sheet = LabourDailySheetHeader.query.get_or_404(sheet_id)
    return render_template("labour/view_daily_sheet.html", sheet=sheet)


@labour_bp.route("/daily-sheet/<int:sheet_id>/approve", methods=["POST"])
@login_required
def approve_daily_sheet(sheet_id):
    sheet = LabourDailySheetHeader.query.get_or_404(sheet_id)
    sheet.status = "APPROVED"
    db.session.commit()
    flash(f"Sheet {sheet.sheet_no} approved.", "success")
    return redirect(url_for("labour.daily_sheet_list"))


@labour_bp.route("/daily-sheet/<int:sheet_id>/delete", methods=["POST"])
@login_required
def delete_daily_sheet(sheet_id):
    sheet = LabourDailySheetHeader.query.get_or_404(sheet_id)
    if sheet.status == "APPROVED":
        flash("Cannot delete approved sheet.", "danger")
        return redirect(url_for("labour.daily_sheet_list"))
    db.session.delete(sheet)
    db.session.commit()
    flash("Daily Sheet deleted.", "success")
    return redirect(url_for("labour.daily_sheet_list"))


# ============================================================
# AJAX ENDPOINTS
# ============================================================

@labour_bp.route("/api/get-labour-details/<int:labour_id>")
@login_required
def get_labour_details(labour_id):
    labour = LabourMaster.query.get_or_404(labour_id)
    return jsonify({
        "id": labour.id,
        "name": labour.labour_name,
        "wage_type": labour.wage_type,
        "daily_rate": labour.daily_wage_rate,
        "labour_type": labour.labour_type.type_name,
        "location_id": labour.location_id
    })


@labour_bp.route("/api/get-item-piece-rate/<int:item_id>")
@login_required
def get_item_piece_rate(item_id):
    item = ItemMaster.query.get_or_404(item_id)
    return jsonify({
        "piece_rate": item.piece_rate or 0,
        "item_name": item.item_name
    })


@labour_bp.route("/reports/costing")
@login_required
def labour_costing_report():
    """Report showing labour cost per item produced"""
    from_date = request.args.get("from_date", date.today().replace(day=1).isoformat())
    to_date = request.args.get("to_date", date.today().isoformat())

    from_date = date.fromisoformat(from_date)
    to_date = date.fromisoformat(to_date)

    # Aggregate by item
    results = db.session.query(
        ItemMaster.item_code,
        ItemMaster.item_name,
        db.func.sum(LabourDailySheetEntryDetail.qty_produced).label("total_qty"),
        db.func.sum(LabourDailySheetEntryDetail.piece_wages).label("piece_wages"),
        db.func.sum(LabourDailySheetEntryDetail.proportionate_wages).label("daily_wages"),
        db.func.sum(LabourDailySheetEntryDetail.hours_worked).label("total_hours")
    ).join(
        ItemMaster,
        LabourDailySheetEntryDetail.item_id == ItemMaster.id
    ).join(
        LabourDailySheetEntry,
        LabourDailySheetEntryDetail.entry_id == LabourDailySheetEntry.id
    ).join(
        LabourDailySheetHeader,
        LabourDailySheetEntry.sheet_id == LabourDailySheetHeader.id
    ).filter(
        LabourDailySheetHeader.sheet_date >= from_date,
        LabourDailySheetHeader.sheet_date <= to_date,
        LabourDailySheetHeader.status == "APPROVED"
    ).group_by(
        ItemMaster.id
    ).all()

    return render_template(
        "labour/costing_report.html",
        results=results,
        from_date=from_date,
        to_date=to_date
    )