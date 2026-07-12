from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for)

from flask_login import login_required
from flask import jsonify

from sqlalchemy import func

from flask import flash

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
from models import CustomerMaster
from models import CustomerPOHeader
from models import CustomerPODetail
from models import TransporterMaster
from models import DestinationMaster
from models import SalesInvoiceHeader
from models import SalesInvoiceDetail
from models import ReceivingNoteHeader
from models import ReceivingNoteDetail
from models import BillSubmissionHeader
from models import BillSubmissionDetail
from models import PaymentReceiptHeader

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
            "Assembled Goods",
            "Finished Goods"
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

            output_qty=float(request.form[
                "output_qty"
            ])
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
            "Assembled Goods",
            "Finished Goods"
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

        receipt = PurchaseReceiptHeader(

            receipt_date=date.fromisoformat(
                request.form["receipt_date"]
            ),

            vendor_id=request.form[
                "vendor_id"
            ],

            location_id=request.form[
                "location_id"
            ],

            invoice_no=request.form[
                "invoice_no"
            ],

            invoice_date=date.fromisoformat(
                request.form["invoice_date"]
            ) if request.form["invoice_date"] else None,

            remarks=request.form[
                "remarks"
            ],

            basic_amount=float(
                request.form["total_basic_amount"]
            ),

            gst_amount=float(
                request.form["total_gst_amount"]
            ),

            invoice_amount=float(
                request.form["total_invoice_amount"]
            )

        )

        db.session.add(receipt)

        db.session.flush()

        item_ids = request.form.getlist(
        "item_id"
        )

        #print(item_ids)

        #print(request.form)

        qtys = request.form.getlist(
            "qty"
        )

        rates = request.form.getlist(
            "rate"
        )

        gst_rates = request.form.getlist(
            "gst_rate"
        )

        basic_amounts = request.form.getlist(
            "basic_amount"
        )

        gst_amounts = request.form.getlist(
            "gst_amount"
        )

        invoice_amounts = request.form.getlist(
            "invoice_amount"
        )

        for item_id, qty, rate, gst_rate, basic, gst, invoice in zip(

        item_ids,

        qtys,

        rates,

        gst_rates,

        basic_amounts,

        gst_amounts,

        invoice_amounts

        ):

            if not item_id:

                continue

            detail = PurchaseReceiptDetail(

                purchase_receipt_id=receipt.id,

                item_id=item_id,

                qty=float(qty),

                rate=float(rate),

                basic_amount=float(basic),

                gst_rate=float(gst_rate),

                gst_amount=float(gst),

                invoice_amount=float(invoice)

            )


            db.session.add(detail)

            ledger = InventoryLedger(

                trans_date=receipt.receipt_date,

                item_id=item_id,

                location_id=receipt.location_id,

                qty_in=float(qty),

                qty_out=0,

                reference_type="PURCHASE",

                reference_id=receipt.id,

                remarks="Purchase Receipt"

            )

            db.session.add(ledger)

        db.session.commit()

        return redirect(
            url_for(
                "masters.purchase_receipt"
            )
        )

    return render_template(

         "add_purchase_receipt.html",

        vendor_list=vendor_list,

        location_list=location_list,

        item_list=item_list

    )

@masters_bp.route(
    "/purchase-receipt/view/<int:id>"
)
@login_required
def view_purchase_receipt(id):

    receipt = PurchaseReceiptHeader.query.get_or_404(id)

    return render_template(

        "view_purchase_receipt.html",

        receipt=receipt

    )

@masters_bp.route(
    "/purchase-receipt/delete/<int:id>"
)
@login_required
def delete_purchase_receipt(id):

    receipt = PurchaseReceiptHeader.query.get_or_404(id)

    InventoryLedger.query.filter_by(

        reference_type="PURCHASE",

        reference_id=receipt.id

    ).delete()

    PurchaseReceiptDetail.query.filter_by(

        purchase_receipt_id=receipt.id

    ).delete()

    db.session.delete(receipt)

    db.session.commit()

    return redirect(
        url_for("masters.purchase_receipt")
    )

@masters_bp.route("/customers")
@login_required
def customers():

    customer_list = CustomerMaster.query.order_by(
        CustomerMaster.customer_name
    ).all()

    return render_template(
        "customers.html",
        customer_list=customer_list
    )

@masters_bp.route(
    "/customers/add",
    methods=["GET", "POST"]
)
@login_required
def add_customer():

    if request.method == "POST":

        last_customer = CustomerMaster.query.order_by(
            CustomerMaster.id.desc()
        ).first()

        if last_customer:

            next_no = last_customer.id + 1

        else:

            next_no = 1

        customer = CustomerMaster(

            customer_code=f"CUS-{next_no:06d}",

            customer_name=request.form[
                "customer_name"
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

            credit_days=int(
                request.form["credit_days"]
            ),

            credit_limit=float(
                request.form["credit_limit"]
            ),

            active="active" in request.form

        )

        db.session.add(customer)

        db.session.commit()

        return redirect(
            url_for(
                "masters.customers"
            )
        )

    return render_template(
        "add_customer.html"
    )

@masters_bp.route(
    "/customers/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_customer(id):

    customer = CustomerMaster.query.get_or_404(id)

    if request.method == "POST":

        customer.customer_name = request.form[
            "customer_name"
        ]

        customer.contact_person = request.form[
            "contact_person"
        ]

        customer.mobile = request.form[
            "mobile"
        ]

        customer.email = request.form[
            "email"
        ]

        customer.gst_no = request.form[
            "gst_no"
        ]

        customer.pan_no = request.form[
            "pan_no"
        ]

        customer.address = request.form[
            "address"
        ]

        customer.city = request.form[
            "city"
        ]

        customer.state = request.form[
            "state"
        ]

        customer.country = request.form[
            "country"
        ]

        customer.pincode = request.form[
            "pincode"
        ]

        customer.credit_days = int(
            request.form["credit_days"]
        )

        customer.credit_limit = float(
            request.form["credit_limit"]
        )

        customer.active = "active" in request.form

        db.session.commit()

        return redirect(
            url_for(
                "masters.customers"
            )
        )

    return render_template(

        "edit_customer.html",

        customer=customer

    )

@masters_bp.route("/customer-po")
@login_required
def customer_po():

    po_list = CustomerPOHeader.query.order_by(
        CustomerPOHeader.order_received_date.desc(),
        CustomerPOHeader.id.desc()
    ).all()

    return render_template(
        "customer_po.html",
        po_list=po_list
    )

@masters_bp.route(
    "/customer-po/add",
    methods=["GET", "POST"]
)
@login_required
def add_customer_po():

    customer_list = CustomerMaster.query.order_by(
        CustomerMaster.customer_name
    ).all()

    item_list = ItemMaster.query.join(
    ProductionStageMaster
    ).filter(
    ProductionStageMaster.stage_name == "Ready for Dispatch"
    ).order_by(
    ItemMaster.item_name
    ).all()

    if request.method == "POST":

            po = CustomerPOHeader(

            customer_id=request.form[
                "customer_id"
            ],

            customer_po_no=request.form[
                "customer_po_no"
            ],

            customer_po_date=date.fromisoformat(

                request.form[
                    "customer_po_date"
                ]

            ),

            order_received_date=date.fromisoformat(

                request.form[
                    "order_received_date"
                ]

            ),

            payment_terms=request.form[
                "payment_terms"
            ],

            freight_terms=request.form[
                "freight_terms"
            ],

            remarks=request.form[
                "remarks"
            ],

            status="OPEN"

            )

            db.session.add(po)

            db.session.flush()

            line_nos = request.form.getlist(
            "line_no"
            )

            item_ids = request.form.getlist(
            "item_id"
)

            qtys = request.form.getlist(
                "qty"
            )

            rates = request.form.getlist(
                "rate"
            )

            freights = request.form.getlist(
                "freight"
            )

            gst_rates = request.form.getlist(
                "gst_rate"
            )

            basics = request.form.getlist(
                "basic_amount"
            )

            gst_amounts = request.form.getlist(
                "gst_amount"
            )

            totals = request.form.getlist(
                "total_amount"
            )

            delivery_dates = request.form.getlist(
                "delivery_date"
            )

            for (

            line_no,

            item_id,

            qty,

            rate,

            freight,

            gst_rate,

            basic,

            gst,

            total,

            delivery_date

            ) in zip(

            line_nos,

            item_ids,

            qtys,

            rates,

            freights,

            gst_rates,

            basics,

            gst_amounts,

            totals,

            delivery_dates

            ):

                if not item_id:

                    continue

                detail = CustomerPODetail(

                    customer_po_header_id=po.id,

                    line_no=line_no,

                    item_id=int(item_id),

                    qty=float(qty),

                    rate=float(rate),

                    freight=float(freight),

                    gst_rate=float(gst_rate),

                    basic_amount=float(basic),

                    gst_amount=float(gst),

                    total_amount=float(total),

                    delivery_date=date.fromisoformat(
                        delivery_date
                    ),

                    produced_qty=0,

                    fg_qty=0,

                    dispatched_qty=0,

                    pending_qty=float(qty),

                    status="OPEN"

                )

                db.session.add(detail)

            db.session.commit()

            return redirect(

                url_for(

                        "masters.customer_po"

                    )

                )
    
    
    return render_template(

        "add_customer_po.html",

        customer_list=customer_list,

        item_list=item_list

    )


@masters_bp.route(
    "/customer-po/view/<int:id>"
)
@login_required
def view_customer_po(id):

    po = CustomerPOHeader.query.get_or_404(id)

    return render_template(

        "view_customer_po.html",

        po=po

    )

@masters_bp.route(
    "/customer-po/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_customer_po(id):

    po = CustomerPOHeader.query.get_or_404(id)

    if po.status == "CANCELLED":

        return redirect(

        url_for(

            "masters.customer_po"

        )

    )

    customer_list = CustomerMaster.query.order_by(
        CustomerMaster.customer_name
    ).all()

    item_list = ItemMaster.query.join(
    ProductionStageMaster
    ).filter(
    ProductionStageMaster.stage_name == "Ready for Dispatch"
    ).order_by(
    ItemMaster.item_name
    ).all()

    if request.method == "POST":

        po.customer_id=request.form["customer_id"]

        po.customer_po_no=request.form["customer_po_no"]

        po.customer_po_date=date.fromisoformat(
            request.form["customer_po_date"]
        )

        po.order_received_date=date.fromisoformat(
            request.form["order_received_date"]
        )

        po.payment_terms=request.form["payment_terms"]

        po.freight_terms=request.form["freight_terms"]

        po.remarks=request.form["remarks"]

        CustomerPODetail.query.filter_by(

        customer_po_header_id=po.id

        ).delete()

        line_nos = request.form.getlist(
            "line_no"
            )

        item_ids = request.form.getlist(
                "item_id"
            )

        qtys = request.form.getlist(
                "qty"
            )

        rates = request.form.getlist(
                "rate"
            )

        freights = request.form.getlist(
                "freight"
            )

        gst_rates = request.form.getlist(
                "gst_rate"
            )

        basics = request.form.getlist(
                "basic_amount"
            )

        gst_amounts = request.form.getlist(
                "gst_amount"
            )

        totals = request.form.getlist(
                "total_amount"
            )

        delivery_dates = request.form.getlist(
                "delivery_date"
            )

        for (

            line_no,

            item_id,

            qty,

            rate,

            freight,

            gst_rate,

            basic,

            gst,

            total,

            delivery_date

            ) in zip(

            line_nos,

            item_ids,

            qtys,

            rates,

            freights,

            gst_rates,

            basics,

            gst_amounts,

            totals,

            delivery_dates

            ):

                if not item_id:

                    continue

                detail = CustomerPODetail(

                    customer_po_header_id=po.id,

                    line_no=line_no,

                    item_id=int(item_id),

                    qty=float(qty),

                    rate=float(rate),

                    freight=float(freight),

                    gst_rate=float(gst_rate),

                    basic_amount=float(basic),

                    gst_amount=float(gst),

                    total_amount=float(total),

                    delivery_date=date.fromisoformat(
                        delivery_date
                    ),

                    produced_qty=0,

                    fg_qty=0,

                    dispatched_qty=0,

                    pending_qty=float(qty),

                    status="OPEN"

                )

                db.session.add(detail)  

        db.session.commit()

        return redirect(

        url_for(

        "masters.customer_po"

        )

        )

    return render_template(

        "edit_customer_po.html",

        po=po,

        customer_list=customer_list,

        item_list=item_list,

        today=date.today().isoformat()

    )


@masters_bp.route(
    "/customer-po/cancel/<int:id>"
)
@login_required
def cancel_customer_po(id):

    po = CustomerPOHeader.query.get_or_404(id)

    po.status = "CANCELLED"

    for row in po.details:

        row.status = "CANCELLED"

    db.session.commit()

    return redirect(

        url_for(

            "masters.customer_po"

        )

    )

@masters_bp.route("/transporter")
@login_required
def transporter():

    transporter_list = TransporterMaster.query.order_by(
        TransporterMaster.transporter_name
    ).all()

    return render_template(
        "transporter.html",
        transporter_list=transporter_list
    )

@masters_bp.route(
    "/transporter/add",
    methods=["GET","POST"]
)
@login_required
def add_transporter():

    if request.method == "POST":

        transporter = TransporterMaster(

            transporter_code=request.form["transporter_code"],

            transporter_name=request.form["transporter_name"],

            contact_person=request.form["contact_person"],

            mobile_no=request.form["mobile_no"],

            email=request.form["email"],

            address=request.form["address"],

            gstin=request.form["gstin"],

            active="active" in request.form

        )

        db.session.add(transporter)

        db.session.commit()

        return redirect(
            url_for("masters.transporter")
        )

    return render_template(
        "add_transporter.html"
    )

@masters_bp.route(
    "/transporter/edit/<int:id>",
    methods=["GET","POST"]
)
@login_required
def edit_transporter(id):

    transporter = TransporterMaster.query.get_or_404(id)

    if request.method == "POST":

        transporter.transporter_code = request.form["transporter_code"]

        transporter.transporter_name = request.form["transporter_name"]

        transporter.contact_person = request.form["contact_person"]

        transporter.mobile_no = request.form["mobile_no"]

        transporter.email = request.form["email"]

        transporter.address = request.form["address"]

        transporter.gstin = request.form["gstin"]

        transporter.active = "active" in request.form

        db.session.commit()

        return redirect(
            url_for("masters.transporter")
        )

    return render_template(
        "edit_transporter.html",
        transporter=transporter
    )

@masters_bp.route(
    "/transporter/view/<int:id>"
)
@login_required
def view_transporter(id):

    print("Inside view transporter")
    print(id)

    transporter = TransporterMaster.query.get_or_404(id)

    return render_template(
        "view_transporter.html",
        transporter=transporter
    )

@masters_bp.route("/destination")
@login_required
def destination():

    destination_list = DestinationMaster.query.order_by(
        DestinationMaster.destination_name
    ).all()

    return render_template(
        "destination.html",
        destination_list=destination_list
    )

@masters_bp.route( "/destination/add", methods=["GET", "POST"] ) 
@login_required
def add_destination():
    if request.method == "POST":
        destination = DestinationMaster(
            destination_name=request.form["destination_name"],
            state_name=request.form["state_name"],
            active="active" in request.form
        )
        db.session.add(destination)
        db.session.commit()
        return redirect( url_for("masters.destination") )
    return render_template("add_destination.html")

@masters_bp.route( "/destination/edit/<int:id>", methods=["GET", "POST"] ) 
@login_required
def edit_destination(id):
    destination = DestinationMaster.query.get_or_404(id)
    if request.method == "POST":
        destination.destination_name = request.form[ "destination_name" ]
        destination.state_name = request.form[ "state_name" ]
        destination.active = "active" in request.form
        db.session.commit()
        return redirect( url_for("masters.destination") )
    return render_template( "edit_destination.html", destination=destination )

@masters_bp.route( "/destination/view/<int:id>" ) 
@login_required
def view_destination(id):
    destination = DestinationMaster.query.get_or_404(id)
    return render_template( "view_destination.html", destination=destination )


@masters_bp.route("/sales-invoice")
@login_required
def sales_invoice():

    invoice_list = SalesInvoiceHeader.query.order_by(
        SalesInvoiceHeader.invoice_date.desc(),
        SalesInvoiceHeader.invoice_no.desc()
    ).all()

    return render_template(
        "sales_invoice.html",
        invoice_list=invoice_list
    )

@masters_bp.route(
    "/sales-invoice/add",
    methods=["GET", "POST"]
)
@login_required
def add_sales_invoice():

    customer_po_list = CustomerPOHeader.query.filter(
        CustomerPOHeader.status.in_(["OPEN", "PARTIAL"])
    ).order_by(
        CustomerPOHeader.customer_po_no
    ).all()

    destination_list = DestinationMaster.query.filter_by(
        active=True
    ).order_by(
        DestinationMaster.destination_name
    ).all()

    location_list = LocationMaster.query.order_by(
    LocationMaster.location_name
    ).all()

    transporter_list = TransporterMaster.query.filter_by(
        active=True
    ).order_by(
        TransporterMaster.transporter_name
    ).all()

    
    
    
    if request.method == "POST":

        invoice = SalesInvoiceHeader(

            invoice_no=request.form["invoice_no"],

            invoice_date = date.fromisoformat(
                request.form["invoice_date"]
            ),

            customer_po_header_id=request.form["customer_po_header_id"],

            customer_id=CustomerPOHeader.query.get(
                request.form["customer_po_header_id"]
            ).customer_id,

            destination_id=request.form["destination_id"],

            transporter_id=request.form["transporter_id"],

            vehicle_no=request.form["vehicle_no"],

            lr_no=request.form["lr_no"],

            location_id=int(
            request.form["location_id"]
            ),

            eway_bill_no=request.form["eway_bill_no"],

            remarks=request.form["remarks"],

            status="Pending RNote"

        )

        db.session.add(invoice)

        db.session.flush()

        po_detail_ids = request.form.getlist("po_detail_id")

        dispatch_qtys = request.form.getlist("dispatch_qty")

        for i in range(len(po_detail_ids)):

            qty=float(dispatch_qtys[i])

            if qty<=0:
                continue

            po_line=CustomerPODetail.query.get(
                po_detail_ids[i]
                )
            
            basic=(

                po_line.rate+

                po_line.freight

            )*qty

            gst=basic*po_line.gst_rate/100

            total=basic+gst

            invoice_line=SalesInvoiceDetail(

                sales_invoice_header_id=invoice.id,

                customer_po_detail_id=po_line.id,

                item_id=po_line.item_id,

                dispatch_qty=qty,

                rate=po_line.rate,

                freight=po_line.freight,

                gst_rate=po_line.gst_rate,

                basic_amount=basic,

                gst_amount=gst,

                total_amount=total

                )

            db.session.add(invoice_line)

            ledger=InventoryLedger(

                trans_date=invoice.invoice_date,

                item_id=po_line.item_id,

                location_id=int(request.form["location_id"]),

                qty_in=0,

                qty_out=qty,

                reference_type="Sales Invoice",

                reference_id=invoice.id,

                remarks=invoice.invoice_no

            )

            db.session.add(ledger)

            # -----------------------------
            # Update Customer PO Detail
            # -----------------------------

            po_line.dispatched_qty += qty

            po_line.pending_qty = (
                po_line.qty -
                po_line.dispatched_qty
            )

            if po_line.pending_qty <= 0:

                po_line.pending_qty = 0

                po_line.status = "CLOSED"

            else:

                po_line.status = "PARTIAL"

        # -----------------------------------
        # Update PO Header Status
        # -----------------------------------

        po_header = CustomerPOHeader.query.get(
            invoice.customer_po_header_id
        )

        all_closed = True

        for line in po_header.details:

            if line.pending_qty > 0:

                all_closed = False
                break

        if all_closed:

            po_header.status = "CLOSED"

        else:

            po_header.status = "PARTIAL"

        db.session.commit()







    return render_template(

        "add_sales_invoice.html",

        customer_po_list=customer_po_list,

        destination_list=destination_list,

        transporter_list=transporter_list,

        location_list=location_list

    )


@masters_bp.route(
    "/sales-invoice/get-po-details/<int:po_id>"
)
@login_required
def get_po_details(po_id):

    po = CustomerPOHeader.query.get_or_404(po_id)

    result = {
        "customer": po.customer.customer_name,
        "lines": []
    }

    for line in po.details:

        inventory = InventoryLedger.query.filter_by(
            item_id=line.item_id
        ).first()

        available_qty = (
        db.session.query(
        db.func.sum(
            InventoryLedger.qty_in -
            InventoryLedger.qty_out
        )
        )
        .filter(
        InventoryLedger.item_id == line.item_id
        )
        .scalar()
        or 0
        )

        result["lines"].append({

            "po_detail_id": line.id,

            "item_name": line.item.item_name,

            "ordered_qty": line.qty,

            "pending_qty": line.pending_qty,

            "rate": line.rate,

            "freight": line.freight,

            "gst_rate": line.gst_rate

        })

    return jsonify(result)



@masters_bp.route(
    "/sales-invoice/view/<int:id>"
)
@login_required
def view_sales_invoice(id):

    invoice = SalesInvoiceHeader.query.get_or_404(id)

    return render_template(
        "view_sales_invoice.html",
        invoice=invoice
    )

'''@masters_bp.route(
    "/sales-invoice/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_sales_invoice(id):

    invoice = SalesInvoiceHeader.query.get_or_404(id)

    customer_po_list = CustomerPOHeader.query.order_by(
        CustomerPOHeader.customer_po_no
    ).all()

    destination_list = DestinationMaster.query.filter_by(
        active=True
    ).order_by(
        DestinationMaster.destination_name
    ).all()

    transporter_list = TransporterMaster.query.filter_by(
        active=True
    ).order_by(
        TransporterMaster.transporter_name
    ).all()

    location_list = LocationMaster.query.filter_by(
        active=True
    ).order_by(
        LocationMaster.location_name
    ).all()

    if request.method == "POST":

        # Save logic will come in next step

        pass

    return render_template(

        "edit_sales_invoice.html",

        invoice=invoice,

        customer_po_list=customer_po_list,

        destination_list=destination_list,

        transporter_list=transporter_list,

        location_list=location_list

    )'''


@masters_bp.route(
    "/sales-invoice/cancel/<int:id>"
)
@login_required
def cancel_sales_invoice(id):

    invoice = SalesInvoiceHeader.query.get_or_404(id)

    if invoice.status == "CANCELLED":

        return redirect(
            url_for("masters.sales_invoice")
        )

    #
    # Reverse inventory
    #

    for line in invoice.details:

        ledger = InventoryLedger(

            trans_date=date.today(),

            item_id=line.item_id,

            location_id=invoice.location_id,

            qty_in=line.dispatch_qty,

            qty_out=0,

            reference_type="Sales Invoice Cancel",

            reference_id=invoice.id,

            remarks=invoice.invoice_no

        )

        db.session.add(ledger)

        #
        # Update PO Detail
        #

        po_line = line.po_detail

        po_line.dispatched_qty -= line.dispatch_qty

        if po_line.dispatched_qty < 0:

            po_line.dispatched_qty = 0

        po_line.pending_qty = (
            po_line.qty -
            po_line.dispatched_qty
        )

        #
        # Line Status
        #

        if po_line.dispatched_qty == 0:

            po_line.status = "OPEN"

        elif po_line.pending_qty == 0:

            po_line.status = "CLOSED"

        else:

            po_line.status = "PARTIAL"

    #
    # Header Status
    #

    po = invoice.customer_po

    if all(
        d.pending_qty == d.qty
        for d in po.details
    ):

        po.status = "OPEN"

    elif all(
        d.pending_qty == 0
        for d in po.details
    ):

        po.status = "CLOSED"

    else:

        po.status = "PARTIAL"

    #
    # Invoice Status
    #

    invoice.status = "CANCELLED"

    db.session.commit()

    return redirect(
        url_for("masters.sales_invoice")
    )


@masters_bp.route("/receiving-note")
@login_required
def receiving_note():

    rnote_list = ReceivingNoteHeader.query.order_by(
        ReceivingNoteHeader.rnote_date.desc(),
        ReceivingNoteHeader.rnote_no.desc()
    ).all()

    return render_template(
        "receiving_note.html",
        rnote_list=rnote_list
    )    

@masters_bp.route(
    "/receiving-note/add",
    methods=["GET", "POST"]
)
@login_required
def add_receiving_note():

    invoice_list = SalesInvoiceHeader.query.filter_by(
        status="Pending RNote"
    ).order_by(
        SalesInvoiceHeader.invoice_date.desc()
    ).all()

    if request.method == "POST":

        rnote = ReceivingNoteHeader(

            rnote_no=request.form["rnote_no"],

            rnote_date=date.fromisoformat(
                request.form["rnote_date"]
            ),

            sales_invoice_header_id=int(
                request.form["sales_invoice_header_id"]
            ),

            customer_id=SalesInvoiceHeader.query.get(
                int(request.form["sales_invoice_header_id"])
            ).customer_id,

            received_by=request.form.get(
                "received_by"
            ),

            remarks=request.form.get(
                "remarks"
            ),

            status="ACTIVE"

        )

        db.session.add(rnote)

        db.session.flush()

        invoice_detail_ids = request.form.getlist(
            "invoice_detail_id"
        )

        item_ids = request.form.getlist(
            "item_id"
        )

        received_qtys = request.form.getlist(
            "received_qty"
        )

        short_qtys = request.form.getlist(
            "short_qty"
        )

        rejected_qtys = request.form.getlist(
            "rejected_qty"
        )   

        for (

            invoice_detail_id,

            item_id,

            received_qty,

            short_qty,

            rejected_qty

        ) in zip(

            invoice_detail_ids,

            item_ids,

            received_qtys,

            short_qtys,

            rejected_qtys

        ):

            invoice_line = SalesInvoiceDetail.query.get(
                int(invoice_detail_id)
            )

            detail = ReceivingNoteDetail(

                receiving_note_header_id=rnote.id,

                sales_invoice_detail_id=int(invoice_detail_id),

                item_id=int(item_id),

                dispatch_qty=invoice_line.dispatch_qty,

                received_qty=float(received_qty),

                short_qty=float(short_qty),

                rejected_qty=float(rejected_qty)

            )

            db.session.add(detail)

        invoice = SalesInvoiceHeader.query.get(
            rnote.sales_invoice_header_id
        )

        invoice.status = "Pending Bill Submission"

        db.session.commit()

        return redirect(

            url_for(

                "masters.receiving_note"

            )

        )

    return render_template(
        "add_receiving_note.html",
        invoice_list=invoice_list
    )

@masters_bp.route(
    "/receiving-note/get-invoice-details/<int:invoice_id>"
)
@login_required
def get_invoice_details(invoice_id):

    invoice = SalesInvoiceHeader.query.get_or_404(invoice_id)

    result = {

        "customer": invoice.customer.customer_name,

        "invoice_no": invoice.invoice_no,

        "invoice_date": invoice.invoice_date.strftime("%d-%m-%Y"),

        "lines": []

    }

    for line in invoice.details:

        result["lines"].append({

            "invoice_detail_id": line.id,

            "item_id": line.item_id,

            "item_name": line.item.item_name,

            "dispatch_qty": line.dispatch_qty

        })

    return jsonify(result)


@masters_bp.route(
    "/receiving-note/cancel/<int:id>"
)
@login_required
def cancel_receiving_note(id):

    rnote = ReceivingNoteHeader.query.get_or_404(id)

    if rnote.status == "CANCELLED":

        return redirect(

            url_for(
                "masters.receiving_note"
            )

        )

    rnote.status = "CANCELLED"

    invoice = SalesInvoiceHeader.query.get(

        rnote.sales_invoice_header_id

    )

    invoice.status = "Pending RNote"

    db.session.commit()

    return redirect(

        url_for(
            "masters.receiving_note"
        )

    )

@masters_bp.route(
    "/receiving-note/view/<int:id>"
)
@login_required
def view_receiving_note(id):

    rnote = ReceivingNoteHeader.query.get_or_404(id)

    return render_template(

        "view_receiving_note.html",

        rnote=rnote

    )

@masters_bp.route("/bill-submission")
@login_required
def bill_submission():

    bill_list = BillSubmissionHeader.query.order_by(
        BillSubmissionHeader.bill_submission_date.desc(),
        BillSubmissionHeader.bill_submission_no.desc()
    ).all()

    return render_template(
        "bill_submission.html",
        bill_list=bill_list
    )


@masters_bp.route(
    "/bill-submission/add",
    methods=["GET", "POST"]
)
@login_required
def add_bill_submission():

    rnote_list = ReceivingNoteHeader.query.filter_by(
        status="ACTIVE"
    ).join(
        SalesInvoiceHeader
    ).filter(
        SalesInvoiceHeader.status == "Pending Bill Submission"
    ).order_by(
        ReceivingNoteHeader.rnote_date.desc()
    ).all()

    if request.method == "POST":

        # Save logic later

        rnote = ReceivingNoteHeader.query.get(

        request.form["receiving_note_header_id"]

        )

        bill = BillSubmissionHeader(

        bill_submission_no=request.form[
            "bill_submission_no"
        ],

        bill_submission_date=date.fromisoformat(

            request.form[
                "bill_submission_date"
            ]

        ),

        receiving_note_header_id=request.form[
            "receiving_note_header_id"
        ],

        sales_invoice_header_id=rnote.sales_invoice_header_id,

        customer_id=rnote.customer_id,

        drr_no=request.form[
            "drr_no"
        ],

        ro_no=request.form[
            "ro_no"
        ],

        ro_date=(

            date.fromisoformat(
                request.form["ro_date"]
            )

            if request.form["ro_date"]

            else None

        ),

        remarks=request.form[
            "remarks"
        ],

        status="OPEN"

    )

        db.session.add(bill)

        db.session.flush()

        grand_total = 0

        for row in rnote.details:

            invoice_line = row.invoice_detail

            basic = (

                invoice_line.rate +

                invoice_line.freight

            ) * row.received_qty

            gst = basic * invoice_line.gst_rate / 100

            total = basic + gst

            grand_total += total

            detail = BillSubmissionDetail(

                bill_submission_header_id=bill.id,

                receiving_note_detail_id=row.id,

                item_id=row.item_id,

                received_qty=row.received_qty,

                rate=invoice_line.rate,

                freight=invoice_line.freight,

                basic_amount=basic,

                gst_amount=gst,

                total_amount=total

            )

            db.session.add(detail)

        bill.bill_amount = grand_total

        invoice = rnote.invoice

        invoice.status = "Bill Submitted"

        rnote.status = "Bill Submitted"

        db.session.commit()

        return redirect(

            url_for(

                "masters.bill_submission"

            )

        )

    return render_template(

        "add_bill_submission.html",

        rnote_list=rnote_list

    )

@masters_bp.route(
    "/bill-submission/get-rnote-details/<int:rnote_id>"
)
@login_required
def get_rnote_details(rnote_id):

    rnote = ReceivingNoteHeader.query.get_or_404(rnote_id)

    result = {

        "customer": rnote.customer.customer_name,

        "invoice_no": rnote.invoice.invoice_no,

        "invoice_date": rnote.invoice.invoice_date.strftime("%d-%m-%Y"),

        "lines": []

    }

    total_received_qty = 0
    total_basic = 0
    total_gst = 0
    total_amount = 0

    for line in rnote.details:

        invoice_line = line.invoice_detail

        basic = (
            invoice_line.rate +
            invoice_line.freight
        ) * line.received_qty

        gst = basic * invoice_line.gst_rate / 100

        total = basic + gst

        total_basic += basic
        total_gst += gst
        total_amount += total
        total_received_qty += line.received_qty

        result["lines"].append({

            "item_name": line.item.item_name,

            "received_qty": line.received_qty,

            "rate": invoice_line.rate,

            "freight": invoice_line.freight,

            "basic_amount": basic,

            "gst_amount": gst,

            "total_amount": total


        })

    result["total_received_qty"] = total_received_qty
    result["total_basic"] = total_basic
    result["total_gst"] = total_gst
    result["grand_total"] = total_amount

    return jsonify(result)

@masters_bp.route(
    "/bill-submission/view/<int:id>"
)
@login_required
def view_bill_submission(id):

    bill = BillSubmissionHeader.query.get_or_404(id)

    return render_template(

        "view_bill_submission.html",

        bill=bill

    )

@masters_bp.route(
    "/bill-submission/cancel/<int:id>"
)
@login_required
def cancel_bill_submission(id):

    bill = BillSubmissionHeader.query.get_or_404(id)

    if bill.status == "CANCELLED":

        flash(
            "Bill already cancelled.",
            "warning"
        )

        return redirect(

            url_for(
                "masters.bill_submission"
            )

        )

    bill.status = "CANCELLED"

    rnote = bill.receiving_note

    invoice = bill.invoice

    rnote.status = "ACTIVE"

    invoice.status = "Pending Bill Submission"

    db.session.commit()

    flash(

        "Bill Submission cancelled successfully.",

        "success"

    )

    return redirect(

        url_for(
            "masters.bill_submission"
        )

    )

######################################################
# PAYMENT
######################################################

@masters_bp.route("/payment")
@login_required
def payment():

    payment_list = PaymentReceiptHeader.query.order_by(

        PaymentReceiptHeader.payment_date.desc(),

        PaymentReceiptHeader.payment_no.desc()

    ).all()

    return render_template(

        "payment.html",

        payment_list=payment_list

    )


@masters_bp.route(
    "/payment/add",
    methods=["GET", "POST"]
)
@login_required
def add_payment():

    bill_list = BillSubmissionHeader.query.filter_by(

        status="OPEN"

    ).order_by(

        BillSubmissionHeader.bill_submission_date.desc()

    ).all()

    if request.method == "POST":

        bill = BillSubmissionHeader.query.get_or_404(

            request.form["bill_submission_header_id"]

        )

        payment = PaymentReceiptHeader(

            payment_no=request.form["payment_no"],

            payment_date=date.fromisoformat(

                request.form["payment_date"]

            ),

            bill_submission_header_id=bill.id,

            sales_invoice_header_id=bill.sales_invoice_header_id,

            customer_id=bill.customer_id,

            bill_amount=bill.bill_amount,

            amount_received=float(
                request.form["amount_received"]
            ),

            tds_deducted=float(
                request.form["tds_deducted"]
            ),

            ld_charges=float(
                request.form["ld_charges"]
            ),

            general_damage_charges=float(
                request.form["general_damage_charges"]
            ),

            other_deductions=float(
                request.form["other_deductions"]
            ),

            #payment_mode=request.form["payment_mode"],

            #bank_name=request.form["bank_name"],

            #utr_no=request.form["utr_no"],

            remarks=request.form["remarks"],

            status="ACTIVE"

        )

        db.session.add(payment)

        bill.status = "PAYMENT RECEIVED"

        invoice = bill.invoice

        invoice.status = "Payment Received"

        db.session.commit()

        return redirect(

            url_for(

                "masters.payment"

            )

        )


    return render_template(

        "add_payment.html",

        bill_list=bill_list

    )

@masters_bp.route(
    "/payment/get-bill-details/<int:bill_id>"
)
@login_required
def get_bill_details(bill_id):

    bill = BillSubmissionHeader.query.get_or_404(bill_id)

    return jsonify({

        "customer": bill.customer.customer_name,

        "invoice_no": bill.invoice.invoice_no,

        "invoice_date": bill.invoice.invoice_date.strftime("%d-%m-%Y"),

        "bill_amount": bill.bill_amount

    })    

@masters_bp.route("/payment/view/<int:id>")
@login_required
def view_payment(id):

    payment = PaymentReceiptHeader.query.get_or_404(id)

    return render_template(

        "view_payment.html",

        payment=payment

    )

@masters_bp.route("/payment/cancel/<int:id>")
@login_required
def cancel_payment(id):

    payment = PaymentReceiptHeader.query.get_or_404(id)

    bill = payment.bill_submission

    invoice = payment.invoice

    bill.status = "OPEN"

    invoice.status = "Bill Submitted"

    db.session.delete(payment)

    db.session.commit()

    flash(

        "Payment cancelled successfully.",

        "success"

    )

    return redirect(

        url_for("masters.payment")

    )