from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for)

from flask_login import login_required

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