from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for)

from flask_login import login_required

from sqlalchemy import func

from datetime import date

from models import db
from models import FinishedGood
from models import ItemMaster
from models import LocationMaster
from models import ProductionStageMaster
from models import RecipeHeader
from models import RecipeInput
from models import RecipeByProduct
from models import ProductionEntry
from models import ProductionEntryDetail
from models import InventoryLedger
from models import OpeningStock
from models import OpeningStockDetail
from models import StockAdjustmentDetail
from models import StockAdjustment
from models import VendorMaster
from models import PurchaseReceiptHeader
from models import PurchaseReceiptDetail


masters_bp = Blueprint(
    "masters",
    __name__
)

@masters_bp.route("/finished-goods")
@login_required
def finished_goods():

    fg_list = FinishedGood.query.order_by(
        FinishedGood.fg_code
        ).all()
    
    return render_template(
        "finished_goods.html", 
        fg_list=fg_list
        )

@masters_bp.route(
    "/finished-goods/add",
    methods=["GET", "POST"]
)
@login_required
def add_finished_good():

    if request.method == "POST":

        fg_code = request.form["fg_code"]
        fg_name = request.form["fg_name"]
        pl_number = request.form["pl_number"]
        uvam_reference = request.form["uvam_reference"]

        fg = FinishedGood(
            fg_code=fg_code,
            fg_name=fg_name,
            pl_number=pl_number,
            uvam_reference=uvam_reference
        )

        db.session.add(fg)
        db.session.commit()

        return redirect(
            url_for("masters.finished_goods")
        )

    return render_template(
        "add_finished_good.html"
    )

@masters_bp.route(
    "/finished-goods/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_finished_good(id):

    fg = FinishedGood.query.get_or_404(id)

    if request.method == "POST":

        fg.fg_code = request.form["fg_code"]
        fg.fg_name = request.form["fg_name"]
        fg.pl_number = request.form["pl_number"]
        fg.uvam_reference = request.form["uvam_reference"]

        db.session.commit()

        return redirect(
            url_for("masters.finished_goods")
        )

    return render_template(
        "edit_finished_good.html",
        fg=fg
    )

@masters_bp.route("/items")
@login_required
def items():

    item_list = ItemMaster.query.order_by(
        ItemMaster.item_code
        ).all()

    return render_template(
        "items.html",
        item_list=item_list
    )

@masters_bp.route(
    "/items/add",
    methods=["GET", "POST"]
)
@login_required
def add_item():

    fg_list = FinishedGood.query.order_by(
        FinishedGood.fg_name
    ).all()

    stage_list = ProductionStageMaster.query.order_by(
    ProductionStageMaster.stage_no
    ).all()

    if request.method == "POST":

        fg_id = request.form.get("finished_good_id")
        item_type = request.form["item_type"]

        if item_type in [
            "Intermediate Material",
            "Assembled Goods"
            ] and not fg_id:

            return "FG Mapping is mandatory for Intermediate Material and Assembled Goods"

        item = ItemMaster(
            item_code=request.form["item_code"],
            item_name=request.form["item_name"],
            item_type=request.form["item_type"],
            unit=request.form["unit"],
            hsn_code=request.form[
                    "hsn_code"
                        ],

            gst_rate=float(
                    request.form[
                    "gst_rate"
                    ]),
            #production_stage=request.form["production_stage"],
            finished_good_id=fg_id if fg_id else None,
            production_stage_id=request.form.get(
            "production_stage_id"
            ) or None
        )

        db.session.add(item)
        db.session.commit()

        return redirect(
            url_for("masters.items")
        )

    return render_template(
        "add_item.html",
        fg_list=fg_list,
        stage_list=stage_list
    )

@masters_bp.route(
    "/items/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_item(id):

    item = ItemMaster.query.get_or_404(id)

    fg_list = FinishedGood.query.order_by(
        FinishedGood.fg_name
    ).all()

    stage_list = ProductionStageMaster.query.order_by(
    ProductionStageMaster.stage_no
    ).all()

    if request.method == "POST":

        fg_id = request.form.get("finished_good_id")
        item_type = request.form["item_type"]

        if item_type in [
            "Intermediate Material",
            "Assembled Goods"
            ] and not fg_id:

            return "FG Mapping is mandatory for Intermediate Material and Assembled Goods"

        item.item_code = request.form["item_code"]
        item.item_name = request.form["item_name"]
        item.item_type = request.form["item_type"]
        item.unit = request.form["unit"]
        item.hsn_code = request.form["hsn_code"]
        item.gst_rate = float(request.form["gst_rate"])
        #item.production_stage = request.form["production_stage"]
        item.production_stage_id = request.form.get(
        "production_stage_id"
        ) or None
        item.finished_good_id = fg_id if fg_id else None

        db.session.commit()

        return redirect(
            url_for("masters.items")
        )

    return render_template(
        "edit_item.html",
        item=item,
        fg_list=fg_list,
        stage_list=stage_list
    )

@masters_bp.route("/locations")
@login_required
def locations():

    location_list = LocationMaster.query.order_by(
        LocationMaster.location_code
    ).all()

    return render_template(
        "locations.html",
        location_list=location_list
    )


@masters_bp.route(
    "/locations/add",
    methods=["GET", "POST"]
)
@login_required
def add_location():

    if request.method == "POST":

        location = LocationMaster(
            location_code=request.form["location_code"],
            location_name=request.form["location_name"]
        )

        db.session.add(location)
        db.session.commit()

        return redirect(
            url_for("masters.locations")
        )

    return render_template(
        "add_location.html"
    )


@masters_bp.route(
    "/locations/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_location(id):

    location = LocationMaster.query.get_or_404(id)

    if request.method == "POST":

        location.location_code = request.form["location_code"]
        location.location_name = request.form["location_name"]

        db.session.commit()

        return redirect(
            url_for("masters.locations")
        )

    return render_template(
        "edit_location.html",
        location=location
    )

@masters_bp.route("/production-stages")
@login_required
def production_stages():

    stage_list = ProductionStageMaster.query.order_by(
        ProductionStageMaster.stage_no
    ).all()

    return render_template(
        "production_stages.html",
        stage_list=stage_list
    )

@masters_bp.route(
    "/production-stages/add",
    methods=["GET","POST"]
)
@login_required
def add_production_stage():

    if request.method == "POST":

        stage = ProductionStageMaster(
            stage_no=request.form["stage_no"],
            stage_name=request.form["stage_name"]
        )

        db.session.add(stage)
        db.session.commit()

        return redirect(
            url_for("masters.production_stages")
        )

    return render_template(
        "add_production_stage.html"
    )

@masters_bp.route(
    "/production-stages/edit/<int:id>",
    methods=["GET","POST"]
)
@login_required
def edit_production_stage(id):

    stage = ProductionStageMaster.query.get_or_404(id)

    if request.method == "POST":

        stage.stage_no = request.form["stage_no"]
        stage.stage_name = request.form["stage_name"]

        db.session.commit()

        return redirect(
            url_for("masters.production_stages")
        )

    return render_template(
        "edit_production_stage.html",
        stage=stage
    )

@masters_bp.route("/recipes")
@login_required
def recipes():

    recipe_list = RecipeHeader.query.all()

    return render_template(
        "recipes.html",
        recipe_list=recipe_list
    )

@masters_bp.route(
    "/recipes/add",
    methods=["GET", "POST"]
)
@login_required
def add_recipe():

    item_list = ItemMaster.query.filter(
        ItemMaster.item_type.in_([
            "Intermediate Material",
            "Assembled Goods"
        ])
    ).order_by(
        ItemMaster.item_name
    ).all()

    stage_list = ProductionStageMaster.query.order_by(
        ProductionStageMaster.stage_no
    ).all()

    if request.method == "POST":

        recipe = RecipeHeader(

            recipe_name=request.form["recipe_name"],

            output_item_id=request.form[
                "output_item_id"
            ],

            production_stage_id=request.form[
                "production_stage_id"
            ],

            output_qty=request.form[
                "output_qty"
            ]
        )

        db.session.add(recipe)

        db.session.commit()

        return redirect(
            url_for("masters.recipes")
        )

    return render_template(
        "add_recipe.html",
        item_list=item_list,
        stage_list=stage_list
    )

@masters_bp.route(
    "/recipes/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_recipe(id):

    recipe = RecipeHeader.query.get_or_404(id)

    item_list = ItemMaster.query.filter(
        ItemMaster.item_type.in_([
            "Intermediate Material",
            "Assembled Goods"
        ])
    ).order_by(
        ItemMaster.item_name
    ).all()

    stage_list = ProductionStageMaster.query.order_by(
        ProductionStageMaster.stage_no
    ).all()

    if request.method == "POST":

        recipe.recipe_name = request.form[
            "recipe_name"
        ]

        recipe.output_item_id = request.form[
            "output_item_id"
        ]

        recipe.production_stage_id = request.form[
            "production_stage_id"
        ]

        recipe.output_qty = request.form[
            "output_qty"
        ]

        db.session.commit()

        return redirect(
            url_for("masters.recipes")
        )

    return render_template(
        "edit_recipe.html",
        recipe=recipe,
        item_list=item_list,
        stage_list=stage_list
    )

@masters_bp.route(
    "/recipes/details/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def recipe_details(id):

    recipe = RecipeHeader.query.get_or_404(id)

    item_list = ItemMaster.query.order_by(
        ItemMaster.item_name
    ).all()

    #inputs = RecipeInput.query.filter_by(
    #    recipe_id=id
    #).all()

    #byproducts = RecipeByProduct.query.filter_by(
    #    recipe_id=id
    #).all()

    input_rows = RecipeInput.query.filter_by(
    recipe_id=id
    ).all()

    byproduct_rows = RecipeByProduct.query.filter_by(
    recipe_id=id
    ).all()

    return render_template(
        "recipe_details.html",
        recipe=recipe,
        item_list=item_list,
        input_rows=input_rows,
        byproduct_rows=byproduct_rows
        #inputs=inputs,
        #byproducts=byproducts
    )

@masters_bp.route(
    "/recipes/details/<int:id>/save",
    methods=["POST"]
)
@login_required
def save_recipe_details(id):

    RecipeInput.query.filter_by(
        recipe_id=id
    ).delete()

    RecipeByProduct.query.filter_by(
        recipe_id=id
    ).delete()

    input_items = request.form.getlist(
        "input_item_id"
    )

    input_qtys = request.form.getlist(
        "input_qty"
    )

    for item_id, qty in zip(
        input_items,
        input_qtys
    ):

        if item_id and qty:

            row = RecipeInput(
                recipe_id=id,
                input_item_id=item_id,
                input_qty=qty
            )

            db.session.add(row)

    by_items = request.form.getlist(
        "byproduct_item_id"
    )

    by_qtys = request.form.getlist(
        "byproduct_qty"
    )

    for item_id, qty in zip(
        by_items,
        by_qtys
    ):

        if item_id and qty:

            row = RecipeByProduct(
                recipe_id=id,
                byproduct_item_id=item_id,
                byproduct_qty=qty
            )

            db.session.add(row)

    db.session.commit()

    return redirect(
        url_for(
            "masters.recipe_details",
            id=id
        )
    )

@masters_bp.route("/production")
@login_required
def production():

    production_list = ProductionEntry.query.order_by(
        ProductionEntry.production_date.desc()
    ).all()

    return render_template(
        "production.html",
        production_list=production_list
    )

@masters_bp.route(
    "/production/add",
    methods=["GET", "POST"]
)
@login_required
def add_production():

    recipe_list = RecipeHeader.query.order_by(
        RecipeHeader.recipe_name
    ).all()

    location_list = LocationMaster.query.order_by(
        LocationMaster.location_name
    ).all()

    fg_list = FinishedGood.query.order_by(
    FinishedGood.fg_name
    ).all()

    if request.method == "POST":

        production = ProductionEntry(

            production_date=date.fromisoformat(
                request.form["production_date"]
            ),

            recipe_id=request.form[
                "recipe_id"
            ],

            production_qty=float(
                request.form[
                    "production_qty"
                ]
            ),

            location_id=request.form[
                "location_id"
            ],

            remarks=request.form[
                "remarks"
            ]
        )

        db.session.add(production)

        db.session.flush()

        recipe = RecipeHeader.query.get(
            production.recipe_id
        )

        factor = (
            production.production_qty
            /
            recipe.output_qty
        )

        for row in recipe.inputs:

            qty = row.input_qty * factor

            detail = ProductionEntryDetail(

                production_entry_id=
                production.id,

                item_id=
                row.input_item_id,

                qty=qty,

                transaction_type="INPUT"
            )

            db.session.add(detail)

            ledger = InventoryLedger(

                trans_date=
                production.production_date,

                item_id=
                row.input_item_id,

                location_id=
                production.location_id,

                qty_out=qty,

                reference_type=
                "PRODUCTION",

                reference_id=
                production.id,

                remarks=
                "Material Consumption"
            )

            db.session.add(ledger)

        output_qty = (
        recipe.output_qty
        * factor
        )

        detail = ProductionEntryDetail(

            production_entry_id=
            production.id,

            item_id=
            recipe.output_item_id,

            qty=output_qty,

            transaction_type="OUTPUT"
        )

        db.session.add(detail)

        ledger = InventoryLedger(

            trans_date=
            production.production_date,

            item_id=
            recipe.output_item_id,

            location_id=
            production.location_id,

            qty_in=output_qty,

            reference_type=
            "PRODUCTION",

            reference_id=
            production.id,

            remarks=
            "Production Output"
        )

        db.session.add(ledger)

        for row in recipe.byproducts:

            qty = row.byproduct_qty * factor

            detail = ProductionEntryDetail(

                production_entry_id=
                production.id,

                item_id=
                row.byproduct_item_id,

                qty=qty,

                transaction_type="SCRAP"
            )

            db.session.add(detail)

            ledger = InventoryLedger(

                trans_date=
                production.production_date,

                item_id=
                row.byproduct_item_id,

                location_id=
                production.location_id,

                qty_in=qty,

                reference_type=
                "PRODUCTION",

                reference_id=
                production.id,

                remarks=
                "Byproduct / Scrap"
            )

            db.session.add(ledger)

        db.session.commit()

        return redirect(
            url_for(
                "masters.production"
            )
        )

    return render_template(
        "add_production.html",
        recipe_list=recipe_list,
        location_list=location_list,
        fg_list=fg_list
    )

@masters_bp.route(
    "/production/view/<int:id>"
)
@login_required
def view_production(id):

    production = ProductionEntry.query.get_or_404(id)

    details = ProductionEntryDetail.query.filter_by(
        production_entry_id=id
    ).all()

    return render_template(
        "view_production.html",
        production=production,
        details=details
    )

@masters_bp.route(
    "/production/delete/<int:id>"
)
@login_required
def delete_production(id):

    production = ProductionEntry.query.get_or_404(id)

    InventoryLedger.query.filter_by(
        reference_type="PRODUCTION",
        reference_id=id
    ).delete()

    ProductionEntryDetail.query.filter_by(
        production_entry_id=id
    ).delete()

    db.session.delete(production)

    db.session.commit()

    return redirect(
        url_for("masters.production")
    )

@masters_bp.route("/inventory")
@login_required
def inventory():

    fg_id = request.args.get(
    "fg_id",
    ""
    )

    item_type = request.args.get(
    "item_type",
    ""
    )

    item_search = request.args.get(
        "item",
        ""
    )

    location_id = request.args.get(
        "location_id",
        ""
    )

    query = (

        db.session.query(

            #ItemMaster.id,
            ItemMaster.id.label("item_id"),

            ItemMaster.item_code,

            ItemMaster.item_name,

            ItemMaster.unit,

            LocationMaster.id.label(
                "location_id"
            ),

            LocationMaster.location_name,

            func.sum(
                InventoryLedger.qty_in
            ).label("received"),

            func.sum(
                InventoryLedger.qty_out
            ).label("issued"),

            (
                func.sum(
                    InventoryLedger.qty_in
                )
                -
                func.sum(
                    InventoryLedger.qty_out
                )
            ).label("stock")

        )

        .join(
            InventoryLedger,
            ItemMaster.id ==
            InventoryLedger.item_id
        )

        .join(
            LocationMaster,
            InventoryLedger.location_id ==
            LocationMaster.id
        )

    )

    if item_search:

        query = query.filter(

            ItemMaster.item_name.ilike(
                f"%{item_search}%"
            )

        )

    if fg_id:

        query = query.filter(
        ItemMaster.finished_good_id == fg_id
    )
        
    if item_type:

        query = query.filter(
        ItemMaster.item_type == item_type
    )

    if location_id:

        query = query.filter(

            InventoryLedger.location_id ==
            location_id

        )

    stock = (

        query.group_by(

            ItemMaster.id,
            ItemMaster.item_code,
            ItemMaster.item_name,
            ItemMaster.unit,
            LocationMaster.id,
            LocationMaster.location_name

        )

        .order_by(
            ItemMaster.item_code
        )

        .all()

    )

    location_list = LocationMaster.query.order_by(

        LocationMaster.location_name

    ).all()

    fg_list = FinishedGood.query.order_by(
    FinishedGood.fg_name
    ).all()

    item_types = [

    row[0]

    for row in db.session.query(
        ItemMaster.item_type
    )
    .distinct()
    .order_by(
        ItemMaster.item_type
    )
    .all()

    ]

    return render_template(

    "inventory.html",

    stock=stock,

    item_search=item_search,

    location_id=location_id,

    location_list=location_list,

    fg_list=fg_list,

    fg_id=fg_id,

    item_types=item_types,

    item_type=item_type

    )

@masters_bp.route("/inventory/<int:item_id>")
@login_required
def inventory_detail(item_id):

    item = ItemMaster.query.get_or_404(item_id)

    ledger_rows = InventoryLedger.query.filter_by(
        item_id=item_id
    ).order_by(
        InventoryLedger.trans_date,
        InventoryLedger.id
    ).all()

    balance = 0

    movement = []

    for row in ledger_rows:

        balance += row.qty_in
        balance -= row.qty_out

        movement.append({

            "date": row.trans_date,

            "location": row.location.location_name,

            "reference": row.reference_type,

            "remarks": row.remarks,

            "qty_in": row.qty_in,

            "qty_out": row.qty_out,

            "balance": balance

        })

    return render_template(

        "inventory_detail.html",

        item=item,

        movement=movement

    )

@masters_bp.route("/opening-stock")
@login_required
def opening_stock():

    opening_list = OpeningStock.query.order_by(
        OpeningStock.opening_date.desc(),
        OpeningStock.id.desc()
    ).all()

    return render_template(
        "opening_stock.html",
        opening_list=opening_list
    )

@masters_bp.route(
    "/opening-stock/add",
    methods=["GET", "POST"]
)
@login_required
def add_opening_stock():

    item_list = ItemMaster.query.order_by(
        ItemMaster.item_name
    ).all()

    location_list = LocationMaster.query.order_by(
        LocationMaster.location_name
    ).all()

    if request.method == "POST":

        opening = OpeningStock(

        opening_date=date.fromisoformat(
            request.form["opening_date"]
        ),

        location_id=request.form[
            "location_id"
        ],

        remarks=request.form[
            "remarks"
        ]
    )

        db.session.add(opening)

        db.session.flush()

        item_ids = request.form.getlist(
            "item_id"
        )

        qtys = request.form.getlist(
            "qty"
        )

        for item_id, qty in zip(
            item_ids,
            qtys
        ):

            if not item_id or not qty:

                continue

            detail = OpeningStockDetail(

                opening_stock_id=
                opening.id,

                item_id=item_id,

                qty=float(qty)

            )

            db.session.add(detail)

            ledger = InventoryLedger(

                trans_date=
                opening.opening_date,

                item_id=item_id,

                location_id=
                opening.location_id,

                qty_in=float(qty),

                qty_out=0,

                reference_type=
                "OPENING",

                reference_id=
                opening.id,

                remarks=
                "Opening Stock"

            )

            db.session.add(ledger)

        db.session.commit()

        return redirect(
            url_for(
                "masters.opening_stock"
            )
        )

    return render_template(

        "add_opening_stock.html",

        item_list=item_list,

        location_list=location_list

    )

@masters_bp.route(
    "/opening-stock/view/<int:id>"
)
@login_required
def view_opening_stock(id):

    opening = OpeningStock.query.get_or_404(id)

    return render_template(

        "view_opening_stock.html",

        opening=opening

    )

@masters_bp.route("/stock-adjustment")
@login_required
def stock_adjustment():

    adjustment_list = StockAdjustment.query.order_by(

        StockAdjustment.adjustment_date.desc(),

        StockAdjustment.id.desc()

    ).all()

    return render_template(

        "stock_adjustment.html",

        adjustment_list=adjustment_list

    )

@masters_bp.route(
    "/stock-adjustment/add",
    methods=["GET", "POST"]
)
@login_required
def add_stock_adjustment():

    item_list = ItemMaster.query.order_by(
        ItemMaster.item_name
    ).all()

    location_list = LocationMaster.query.order_by(
        LocationMaster.location_name
    ).all()

    if request.method == "POST":

        adjustment = StockAdjustment(

            adjustment_date=date.fromisoformat(
                request.form["adjustment_date"]
            ),

            location_id=request.form["location_id"],

            remarks=request.form["remarks"]

        )

        db.session.add(adjustment)

        db.session.flush()

        item_ids = request.form.getlist("item_id")

        types = request.form.getlist(
            "adjustment_type"
        )

        qtys = request.form.getlist("qty")

        for item_id, adj_type, qty in zip(

            item_ids,

            types,

            qtys

        ):

            if not item_id or not qty:

                continue

            detail = StockAdjustmentDetail(

                stock_adjustment_id=adjustment.id,

                item_id=item_id,

                adjustment_type=adj_type,

                qty=float(qty)

            )

            db.session.add(detail)

            ledger = InventoryLedger(

                trans_date=adjustment.adjustment_date,

                item_id=item_id,

                location_id=adjustment.location_id,

                qty_in=float(qty)
                if adj_type == "INCREASE"
                else 0,

                qty_out=float(qty)
                if adj_type == "DECREASE"
                else 0,

                reference_type="ADJUSTMENT",

                reference_id=adjustment.id,

                remarks="Stock Adjustment"

            )

            db.session.add(ledger)

        db.session.commit()

        return redirect(
            url_for(
                "masters.stock_adjustment"
            )
        )

    return render_template(

        "add_stock_adjustment.html",

        item_list=item_list,

        location_list=location_list

    )

@masters_bp.route(
    "/stock-adjustment/view/<int:id>"
)
@login_required
def view_stock_adjustment(id):

    adjustment = StockAdjustment.query.get_or_404(id)

    return render_template(

        "view_stock_adjustment.html",

        adjustment=adjustment

    )

@masters_bp.route("/vendors")
@login_required
def vendors():

    vendor_list = VendorMaster.query.order_by(
        VendorMaster.vendor_name
    ).all()

    return render_template(
        "vendors.html",
        vendor_list=vendor_list
    )


@masters_bp.route(
    "/vendors/add",
    methods=["GET", "POST"]
)
@login_required
def add_vendor():

    if request.method == "POST":

        vendor = VendorMaster(


            vendor_name=request.form[
                "vendor_name"
            ],

            contact_person=request.form[
                "contact_person"
            ],

            mobile=request.form[
                "mobile"
            ],

            email=request.form[
                "email"
            ],

            gst_no=request.form[
                "gst_no"
            ],

            pan_no=request.form[
                "pan_no"
            ],

            address=request.form[
                "address"
            ],

            city=request.form[
                "city"
            ],

            state=request.form[
                "state"
            ],

            country=request.form[
                "country"
            ],

            pincode=request.form[
                "pincode"
            ],

            active="active" in request.form

        )

        db.session.add(vendor)
        db.session.flush()
        vendor.vendor_code = f"V{vendor.id:05d}"

        db.session.commit()

        return redirect(
            url_for(
                "masters.vendors"
            )
        )

    return render_template(
        "add_vendor.html"
    )


@masters_bp.route(
    "/vendors/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_vendor(id):

    vendor = VendorMaster.query.get_or_404(id)

    if request.method == "POST":

        vendor.vendor_name = request.form[
            "vendor_name"
        ]

        vendor.contact_person = request.form[
            "contact_person"
        ]

        vendor.mobile = request.form[
            "mobile"
        ]

        vendor.email = request.form[
            "email"
        ]

        vendor.gst_no = request.form[
            "gst_no"
        ]

        vendor.pan_no = request.form[
            "pan_no"
        ]

        vendor.address = request.form[
            "address"
        ]

        vendor.city = request.form[
            "city"
        ]

        vendor.state = request.form[
            "state"
        ]

        vendor.country = request.form[
            "country"
        ]

        vendor.pincode = request.form[
            "pincode"
        ]

        vendor.active = "active" in request.form

        db.session.commit()

        return redirect(
            url_for(
                "masters.vendors"
            )
        )

    return render_template(
        "edit_vendor.html",
        vendor=vendor
    )

@masters_bp.route("/purchase-receipt")
@login_required
def purchase_receipt():

    receipt_list = PurchaseReceiptHeader.query.order_by(
        PurchaseReceiptHeader.receipt_date.desc(),
        PurchaseReceiptHeader.id.desc()
    ).all()

    return render_template(
        "purchase_receipt.html",
        receipt_list=receipt_list
    )

@masters_bp.route(
    "/purchase-receipt/add",
    methods=["GET", "POST"]
)
@login_required
def add_purchase_receipt():

    vendor_list = VendorMaster.query.order_by(
        VendorMaster.vendor_name
    ).all()

    location_list = LocationMaster.query.order_by(
        LocationMaster.location_name
    ).all()

    item_list = ItemMaster.query.order_by(
        ItemMaster.item_name
    ).all()

    if request.method == "POST":

        # Save logic will be added next

        pass

    return render_template(

        "add_purchase_receipt.html",

        vendor_list=vendor_list,

        location_list=location_list,

        item_list=item_list

    )



