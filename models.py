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

    hsn_code = db.Column(
    db.String(20)
    )

    gst_rate = db.Column(
    db.Float,
    default=18
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

class InventoryLedger(db.Model):

    __tablename__ = "inventory_ledger"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    trans_date = db.Column(
        db.Date,
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    location_id = db.Column(
        db.Integer,
        db.ForeignKey("location_master.id"),
        nullable=False
    )

    qty_in = db.Column(
        db.Float,
        default=0
    )

    qty_out = db.Column(
        db.Float,
        default=0
    )

    reference_type = db.Column(
        db.String(50)
    )

    reference_id = db.Column(
        db.Integer
    )

    remarks = db.Column(
        db.String(500)
    )

    item = db.relationship(
        "ItemMaster"
    )

    location = db.relationship(
        "LocationMaster"
    )

class ProductionEntry(db.Model):

    __tablename__ = "production_entry"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    production_date = db.Column(
        db.Date,
        nullable=False
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipe_header.id"),
        nullable=False
    )

    production_qty = db.Column(
        db.Float,
        nullable=False
    )

    location_id = db.Column(
        db.Integer,
        db.ForeignKey("location_master.id"),
        nullable=False
    )

    remarks = db.Column(
        db.String(500)
    )

    recipe = db.relationship(
        "RecipeHeader"
    )

    location = db.relationship(
        "LocationMaster"
    )

    details = db.relationship(
    "ProductionEntryDetail",
    backref="production_entry",
    cascade="all, delete-orphan"
    )

class ProductionEntryDetail(db.Model):

    __tablename__ = "production_entry_detail"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    production_entry_id = db.Column(
        db.Integer,
        db.ForeignKey("production_entry.id"),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    qty = db.Column(
        db.Float,
        nullable=False
    )

    transaction_type = db.Column(
        db.String(20),
        nullable=False
    )
    # INPUT
    # OUTPUT
    # SCRAP

    item = db.relationship(
        "ItemMaster"
    )

class OpeningStock(db.Model):

    __tablename__ = "opening_stock"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    opening_date = db.Column(
        db.Date,
        nullable=False
    )

    location_id = db.Column(
        db.Integer,
        db.ForeignKey("location_master.id"),
        nullable=False
    )

    remarks = db.Column(
        db.String(500)
    )

    location = db.relationship(
        "LocationMaster"
    )

    details = db.relationship(
        "OpeningStockDetail",
        backref="opening_stock",
        cascade="all, delete-orphan"
    )


class OpeningStockDetail(db.Model):

    __tablename__ = "opening_stock_detail"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    opening_stock_id = db.Column(
        db.Integer,
        db.ForeignKey("opening_stock.id"),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    qty = db.Column(
        db.Float,
        nullable=False
    )

    item = db.relationship(
        "ItemMaster"
    )

class StockAdjustment(db.Model):

    __tablename__ = "stock_adjustment"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    adjustment_date = db.Column(
        db.Date,
        nullable=False
    )

    location_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "location_master.id"
        ),
        nullable=False
    )

    remarks = db.Column(
        db.String(500)
    )

    location = db.relationship(
        "LocationMaster"
    )

    details = db.relationship(

        "StockAdjustmentDetail",

        backref="stock_adjustment",

        cascade="all, delete-orphan"

    )

class StockAdjustmentDetail(db.Model):

    __tablename__ = "stock_adjustment_detail"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    stock_adjustment_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "stock_adjustment.id"
        ),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "item_master.id"
        ),
        nullable=False
    )

    adjustment_type = db.Column(
        db.String(20),
        nullable=False
    )
    # INCREASE
    # DECREASE

    qty = db.Column(
        db.Float,
        nullable=False
    )

    item = db.relationship(
        "ItemMaster"
    )

class VendorMaster(db.Model):

    __tablename__ = "vendor_master"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    vendor_code = db.Column(
        db.String(20),
        unique=True,
        nullable=True
    )

    vendor_name = db.Column(
        db.String(200),
        nullable=False
    )

    contact_person = db.Column(
        db.String(100)
    )

    mobile = db.Column(
        db.String(20)
    )

    email = db.Column(
        db.String(100)
    )

    gst_no = db.Column(
        db.String(30)
    )

    pan_no = db.Column(
        db.String(20)
    )

    address = db.Column(
        db.String(500)
    )

    city = db.Column(
        db.String(100)
    )

    state = db.Column(
        db.String(100)
    )

    country = db.Column(
        db.String(100),
        default="India"
    )

    pincode = db.Column(
        db.String(20)
    )

    active = db.Column(
        db.Boolean,
        default=True
    )
class PurchaseReceiptHeader(db.Model):

    __tablename__ = "purchase_receipt_header"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    receipt_date = db.Column(
        db.Date,
        nullable=False
    )

    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey("vendor_master.id"),
        nullable=False
    )

    location_id = db.Column(
        db.Integer,
        db.ForeignKey("location_master.id"),
        nullable=False
    )

    invoice_no = db.Column(
        db.String(100)
    )

    invoice_date = db.Column(
        db.Date
    )

    remarks = db.Column(
        db.String(500)
    )

    vendor = db.relationship(
        "VendorMaster"
    )

    location = db.relationship(
        "LocationMaster"
    )

    basic_amount = db.Column(
    db.Float,
    default=0
    )

    gst_amount = db.Column(
    db.Float,
    default=0
    )

    invoice_amount = db.Column(
    db.Float,
    default=0
    )

    details = db.relationship(
        "PurchaseReceiptDetail",
        backref="receipt",
        cascade="all, delete-orphan"
    )

class PurchaseReceiptDetail(db.Model):

    __tablename__ = "purchase_receipt_detail"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    purchase_receipt_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "purchase_receipt_header.id"
        ),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    qty = db.Column(
        db.Float,
        nullable=False
    )

    rate = db.Column(
        db.Float,
        default=0
    )

    basic_amount = db.Column(db.Float, default=0)

    gst_rate = db.Column(db.Float, default=0)

    gst_amount = db.Column(db.Float, default=0)

    invoice_amount = db.Column(db.Float, default=0)

    item = db.relationship(
        "ItemMaster"
    )

class CustomerMaster(db.Model):

    __tablename__ = "customer_master"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_code = db.Column(
        db.String(20),
        unique=True,
        nullable=True
    )

    customer_name = db.Column(
        db.String(200),
        nullable=False
    )

    contact_person = db.Column(
        db.String(100)
    )

    mobile = db.Column(
        db.String(20)
    )

    email = db.Column(
        db.String(100)
    )

    gst_no = db.Column(
        db.String(30)
    )

    pan_no = db.Column(
        db.String(20)
    )

    address = db.Column(
        db.String(500)
    )

    city = db.Column(
        db.String(100)
    )

    state = db.Column(
        db.String(100)
    )

    country = db.Column(
        db.String(100),
        default="India"
    )

    pincode = db.Column(
        db.String(20)
    )

    credit_days = db.Column(
        db.Integer,
        default=30
    )

    credit_limit = db.Column(
        db.Float,
        default=0
    )

    active = db.Column(
        db.Boolean,
        default=True
    )