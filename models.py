from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

class FinishedGood(db.Model):

    __tablename__ = "finished_goods"

    id = db.Column(db.Integer, primary_key=True)

    fg_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    fg_name = db.Column(
        db.String(200),
        nullable=False
    )

    pl_number = db.Column(
        db.String(100),
        nullable=True
    )

    uvam_reference = db.Column(
        db.String(500),
        nullable=True
    )

    items = db.relationship(
    "ItemMaster",
    backref="finished_good",
    lazy=True
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

class ItemMaster(db.Model):
    __tablename__ = "item_master"

    id = db.Column(db.Integer, primary_key=True)

    item_code = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    item_name = db.Column(
        db.String(255),
        nullable=False
    )

    item_type = db.Column(
        db.String(50),
        nullable=False
    )

    production_stage = db.Column(
    db.String(100)
    )

    production_stage_id = db.Column(
    db.Integer,
    db.ForeignKey(
        "production_stage_master.id"
    ),
    nullable=True
    )

    production_stage_rel = db.relationship(
    "ProductionStageMaster"
    )

    unit = db.Column(
        db.String(20),
        nullable=False
    )

    finished_good_id = db.Column(
    db.Integer,
    db.ForeignKey("finished_goods.id"),
    nullable=True
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

class LocationMaster(db.Model):

    __tablename__ = "location_master"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    location_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    location_name = db.Column(
        db.String(100),
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

class ProductionStageMaster(db.Model):

    __tablename__ = "production_stage_master"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    stage_no = db.Column(
        db.Integer,
        nullable=False
    )

    stage_name = db.Column(
        db.String(100),
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

class RecipeHeader(db.Model):

    __tablename__ = "recipe_header"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    output_item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    output_qty = db.Column(
        db.Float,
        nullable=False,
        default=1
    )

    recipe_name = db.Column(
        db.String(200)
    )

    production_stage_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "production_stage_master.id"
        )
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    output_item = db.relationship(
        "ItemMaster"
    )

    production_stage = db.relationship(
        "ProductionStageMaster"
    )

    inputs = db.relationship(
    "RecipeInput",
    backref="recipe",
    cascade="all, delete-orphan"
    )

    byproducts = db.relationship(
    "RecipeByProduct",
    backref="recipe",
    cascade="all, delete-orphan"
    )

class RecipeInput(db.Model):

    __tablename__ = "recipe_input"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipe_header.id"),
        nullable=False
    )

    input_item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    input_qty = db.Column(
        db.Float,
        nullable=False
    )

    input_item = db.relationship(
    "ItemMaster"
    )

class RecipeByProduct(db.Model):

    __tablename__ = "recipe_byproduct"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipe_header.id"),
        nullable=False
    )

    byproduct_item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    byproduct_qty = db.Column(
        db.Float,
        nullable=False
    )

    byproduct_item = db.relationship(
    "ItemMaster"
    )