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

    piece_rate = db.Column(
        db.Float,
        default=0,
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

    unit_cost = db.Column(
    db.Float,
    default=0
    )

    value_in = db.Column(
        db.Float,
        default=0
    )

    value_out = db.Column(
        db.Float,
        default=0
    )

    running_qty = db.Column(
        db.Float,
        default=0
    )

    running_value = db.Column(
        db.Float,
        default=0
    )

    weighted_average_rate = db.Column(
        db.Float,
        default=0
    )

    transaction_value = db.Column(
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

    rate = db.Column(
    db.Float,
    nullable=False,
    default=0
    )

    value = db.Column(
        db.Float,
        nullable=False,
        default=0
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

class CustomerPOHeader(db.Model):

    __tablename__ = "customer_po_header"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer_master.id"),
        nullable=False
    )

    customer_po_no = db.Column(
        db.String(100),
        nullable=False
    )

    customer_po_date = db.Column(
        db.Date,
        nullable=False
    )

    order_received_date = db.Column(
        db.Date,
        nullable=False
    )

    payment_terms = db.Column(
        db.String(200)
    )

    freight_terms = db.Column(
        db.String(200)
    )

    remarks = db.Column(
        db.String(500)
    )

    status = db.Column(
        db.String(20),
        default="OPEN"
    )

    customer = db.relationship(
        "CustomerMaster"
    )

    details = db.relationship(

        "CustomerPODetail",

        backref="customer_po",

        cascade="all, delete-orphan"

    )

class CustomerPODetail(db.Model):

    __tablename__ = "customer_po_detail"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_po_header_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "customer_po_header.id"
        ),
        nullable=False
    )

    line_no = db.Column(
        db.String(30)
    )

    item_id = db.Column(
    db.Integer,
    db.ForeignKey(
        "item_master.id"
    ),
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

    freight = db.Column(
        db.Float,
        default=0
    )

    gst_rate = db.Column(
        db.Float,
        default=18
    )

    basic_amount = db.Column(
        db.Float,
        default=0
    )

    gst_amount = db.Column(
        db.Float,
        default=0
    )

    total_amount = db.Column(
        db.Float,
        default=0
    )

    delivery_date = db.Column(
        db.Date
    )

    produced_qty = db.Column(
        db.Float,
        default=0
    )

    fg_qty = db.Column(
        db.Float,
        default=0
    )

    dispatched_qty = db.Column(
        db.Float,
        default=0
    )

    pending_qty = db.Column(
        db.Float,
        default=0
    )

    status = db.Column(
        db.String(20),
        default="OPEN"
    )

    item = db.relationship(
        "ItemMaster"
    )

class TransporterMaster(db.Model):

    __tablename__ = "transporter_master"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    transporter_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    transporter_name = db.Column(
        db.String(200),
        nullable=False
    )

    contact_person = db.Column(
        db.String(100)
    )

    mobile_no = db.Column(
        db.String(20)
    )

    email = db.Column(
        db.String(100)
    )

    address = db.Column(
        db.String(500)
    )

    gstin = db.Column(
        db.String(20)
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

class DestinationMaster(db.Model): 
    __tablename__ = "destination_master" 
    
    id = db.Column( db.Integer, primary_key=True ) 
    
    destination_name = db.Column( db.String(200), nullable=False, unique=True ) 
    
    state_name = db.Column( db.String(100) ) 
    
    active = db.Column( db.Boolean, default=True )

class SalesInvoiceHeader(db.Model):

    __tablename__ = "sales_invoice_header"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    invoice_no = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    invoice_date = db.Column(
        db.Date,
        nullable=False
    )

    customer_po_header_id = db.Column(
        db.Integer,
        db.ForeignKey("customer_po_header.id"),
        nullable=False
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer_master.id"),
        nullable=False
    )

    destination_id = db.Column(
        db.Integer,
        db.ForeignKey("destination_master.id"),
        nullable=False
    )

    transporter_id = db.Column(
        db.Integer,
        db.ForeignKey("transporter_master.id"),
        nullable=False
    )

    vehicle_no = db.Column(
        db.String(50)
    )

    lr_no = db.Column(
        db.String(100)
    )

    eway_bill_no = db.Column(
        db.String(100)
    )

    location_id = db.Column(
    db.Integer,
    db.ForeignKey("location_master.id"),
    nullable=False
    )

    remarks = db.Column(
        db.String(500)
    )

    status = db.Column(
        db.String(30),
        default="Pending RNote"
    )

    customer = db.relationship("CustomerMaster")

    customer_po = db.relationship("CustomerPOHeader")

    destination = db.relationship("DestinationMaster")

    transporter = db.relationship("TransporterMaster")

    location = db.relationship("LocationMaster")

    details = db.relationship(
        "SalesInvoiceDetail",
        backref="invoice",
        cascade="all, delete-orphan"
    )

    

class SalesInvoiceDetail(db.Model):

    __tablename__ = "sales_invoice_detail"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sales_invoice_header_id = db.Column(
        db.Integer,
        db.ForeignKey("sales_invoice_header.id"),
        nullable=False
    )

    customer_po_detail_id = db.Column(
        db.Integer,
        db.ForeignKey("customer_po_detail.id"),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    dispatch_qty = db.Column(
        db.Float,
        nullable=False
    )

    rate = db.Column(
        db.Float,
        default=0
    )

    freight = db.Column(
        db.Float,
        default=0
    )

    gst_rate = db.Column(
        db.Float,
        default=18
    )

    basic_amount = db.Column(
        db.Float,
        default=0
    )

    gst_amount = db.Column(
        db.Float,
        default=0
    )

    total_amount = db.Column(
        db.Float,
        default=0
    )

    item = db.relationship("ItemMaster")

    po_detail = db.relationship("CustomerPODetail")

class ReceivingNoteHeader(db.Model):

    __tablename__ = "receiving_note_header"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    rnote_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    rnote_date = db.Column(
        db.Date,
        nullable=False
    )

    sales_invoice_header_id = db.Column(
        db.Integer,
        db.ForeignKey("sales_invoice_header.id"),
        nullable=False
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer_master.id"),
        nullable=False
    )

    received_by = db.Column(
        db.String(150)
    )

    remarks = db.Column(
        db.String(500)
    )

    status = db.Column(
        db.String(30),
        default="OPEN"
    )

    invoice = db.relationship(
        "SalesInvoiceHeader"
    )

    customer = db.relationship(
        "CustomerMaster"
    )

    details = db.relationship(

    "ReceivingNoteDetail",

    backref="receiving_note",

    cascade="all, delete-orphan"

    )

class ReceivingNoteDetail(db.Model):

    __tablename__ = "receiving_note_detail"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    receiving_note_header_id = db.Column(
        db.Integer,
        db.ForeignKey("receiving_note_header.id"),
        nullable=False
    )

    sales_invoice_detail_id = db.Column(
        db.Integer,
        db.ForeignKey("sales_invoice_detail.id"),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    dispatch_qty = db.Column(
        db.Float,
        nullable=False
    )

    received_qty = db.Column(
        db.Float,
        default=0
    )

    rejected_qty = db.Column(
        db.Float,
        default=0
    )

    short_qty = db.Column(
        db.Float,
        default=0
    )

    remarks = db.Column(
        db.String(300)
    )

    item = db.relationship("ItemMaster")

    invoice_detail = db.relationship("SalesInvoiceDetail")

class BillSubmissionHeader(db.Model):

    __tablename__ = "bill_submission_header"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    bill_submission_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    bill_submission_date = db.Column(
        db.Date,
        nullable=False
    )

    receiving_note_header_id = db.Column(
        db.Integer,
        db.ForeignKey("receiving_note_header.id"),
        nullable=False
    )

    sales_invoice_header_id = db.Column(
        db.Integer,
        db.ForeignKey("sales_invoice_header.id"),
        nullable=False
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer_master.id"),
        nullable=False
    )

    drr_no = db.Column(
        db.String(100)
    )

    ro_no = db.Column(
        db.String(100)
    )

    ro_date = db.Column(
        db.Date
    )

    bill_amount = db.Column(
        db.Float,
        default=0
    )

    remarks = db.Column(
        db.String(500)
    )

    status = db.Column(
        db.String(30),
        default="ACTIVE"
    )

    customer = db.relationship(
        "CustomerMaster"
    )

    invoice = db.relationship(
        "SalesInvoiceHeader"
    )

    receiving_note = db.relationship(
        "ReceivingNoteHeader"
    )

    details = db.relationship(

        "BillSubmissionDetail",

        backref="bill_submission",

        cascade="all, delete-orphan"

    )

class BillSubmissionDetail(db.Model):

    __tablename__ = "bill_submission_detail"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    bill_submission_header_id = db.Column(
        db.Integer,
        db.ForeignKey("bill_submission_header.id"),
        nullable=False
    )

    receiving_note_detail_id = db.Column(
        db.Integer,
        db.ForeignKey("receiving_note_detail.id"),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    received_qty = db.Column(
        db.Float,
        nullable=False
    )

    rate = db.Column(
        db.Float
    )

    freight = db.Column(
        db.Float
    )

    gst_rate = db.Column(
        db.Float
    )

    basic_amount = db.Column(
        db.Float
    )

    gst_amount = db.Column(
        db.Float
    )

    total_amount = db.Column(
        db.Float
    )

    item = db.relationship(
        "ItemMaster"
    )

    rnote_detail = db.relationship(
        "ReceivingNoteDetail"
    )

class PaymentReceiptHeader(db.Model):

    __tablename__ = "payment_receipt_header"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    payment_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    payment_date = db.Column(
        db.Date,
        nullable=False
    )

    bill_submission_header_id = db.Column(
        db.Integer,
        db.ForeignKey("bill_submission_header.id"),
        nullable=False
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer_master.id"),
        nullable=False
    )

    sales_invoice_header_id = db.Column(
        db.Integer,
        db.ForeignKey("sales_invoice_header.id"),
        nullable=False
    )

    bill_amount = db.Column(
        db.Float,
        default=0
    )

    amount_received = db.Column(
        db.Float,
        default=0
    )

    tds_deducted = db.Column(
        db.Float,
        default=0
    )

    ld_charges = db.Column(
        db.Float,
        default=0
    )

    general_damage_charges = db.Column(
        db.Float,
        default=0
    )

    other_deductions = db.Column(
        db.Float,
        default=0
    )

    '''payment_mode = db.Column(
        db.String(30)
    )

    bank_name = db.Column(
        db.String(100)
    )

    utr_no = db.Column(
        db.String(100)
    )'''

    remarks = db.Column(
        db.String(500)
    )

    status = db.Column(
        db.String(30),
        default="ACTIVE"
    )

    customer = db.relationship("CustomerMaster")

    invoice = db.relationship("SalesInvoiceHeader")

    bill_submission = db.relationship("BillSubmissionHeader")

class JobWorkHeader(db.Model):

    __tablename__ = "job_work_header"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    jobwork_no = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    jobwork_date = db.Column(
        db.Date,
        nullable=False
    )

    expected_return_date = db.Column(
    db.Date,
    nullable = True
    )

    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey("vendor_master.id"),
        nullable=False
    )

    location_id = db.Column(
        db.Integer,
        db.ForeignKey("location_master.id"),
        nullable=True
    )

    output_item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    planned_output_qty = db.Column(
        db.Float,
        default=0
    )

    job_work_cost = db.Column(
        db.Float,
        default=0
    )

    status = db.Column(
        db.String(20),
        default="Open"
    )

    # Open -> Issued -> Partially Received -> Received -> Cancelled

    remarks = db.Column(
        db.String(300)
    )

    vendor = db.relationship(
        "VendorMaster"
    )

    location = db.relationship(
        "LocationMaster"
    )

    output_item = db.relationship(
        "ItemMaster"
    )

    receipts = db.relationship(
        "JobWorkReceipt",
        backref="jobwork",
        cascade="all, delete-orphan"
    )

    

class JobWorkDetail(db.Model):

    __tablename__ = "job_work_detail"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    job_work_id = db.Column(
        db.Integer,
        db.ForeignKey("job_work_header.id"),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    line_type = db.Column(
        db.String(20),
        nullable=False
    )
    # INPUT
    # OUTPUT
    # SCRAP

    expected_qty = db.Column(
        db.Float,
        default=0
    )

    actual_qty = db.Column(
        db.Float,
        default=0
    )

    rate = db.Column(
        db.Float,
        default=0
    )

    value = db.Column(
        db.Float,
        default=0
    )

    remarks = db.Column(
        db.String(250)
    )

    item = db.relationship(
        "ItemMaster"
    )

    jobwork = db.relationship(
        "JobWorkHeader",
        backref="jobwork_details"
    )


class JobWorkLedger(db.Model):

    __tablename__ = "job_work_ledger"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    job_work_id = db.Column(
        db.Integer,
        db.ForeignKey("job_work_header.id"),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    issued_qty = db.Column(
        db.Float,
        default=0
    )

    received_qty = db.Column(
        db.Float,
        default=0
    )

    balance_qty = db.Column(
        db.Float,
        default=0
    )

    issued_rate = db.Column(
        db.Float,
        default=0
    )

    issued_value = db.Column(
        db.Float,
        default=0
    )

    line_type = db.Column(
        db.String(20)
    )
    # INPUT
    # SCRAP

    item = db.relationship(
        "ItemMaster"
    )

    jobwork = db.relationship(
        "JobWorkHeader",
        backref="ledger"
    )

class JobWorkReceipt(db.Model):

    __tablename__ = "job_work_receipt"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    receipt_no = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    receipt_date = db.Column(
        db.Date,
        nullable=False
    )

    job_work_id = db.Column(
        db.Integer,
        db.ForeignKey("job_work_header.id"),
        nullable=False
    )

    location_id = db.Column(
        db.Integer,
        db.ForeignKey("location_master.id"),
        nullable=False
    )

    output_qty_received = db.Column(
        db.Float,
        default=0
    )

    output_qty_rejected = db.Column(
        db.Float,
        default=0
    )

    scrap_qty_received = db.Column(
        db.Float,
        default=0
    )

    job_work_cost = db.Column(
        db.Float,
        default=0
    )

    total_cost = db.Column(
        db.Float,
        default=0
    )

    remarks = db.Column(
        db.String(500)
    )

    location = db.relationship(
        "LocationMaster"
    )

    details = db.relationship(
        "JobWorkReceiptDetail",
        backref="receipt",
        cascade="all, delete-orphan"
    )


class JobWorkReceiptDetail(db.Model):

    __tablename__ = "job_work_receipt_detail"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    job_work_receipt_id = db.Column(
        db.Integer,
        db.ForeignKey("job_work_receipt.id"),
        nullable=False
    )

    job_work_detail_id = db.Column(
        db.Integer,
        db.ForeignKey("job_work_detail.id"),
        nullable=False
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey("item_master.id"),
        nullable=False
    )

    line_type = db.Column(
        db.String(20),
        nullable=False
    )
    # INPUT
    # SCRAP

    issued_qty = db.Column(
        db.Float,
        default=0
    )

    received_qty = db.Column(
        db.Float,
        default=0
    )

    rejected_qty = db.Column(
        db.Float,
        default=0
    )

    rate = db.Column(
        db.Float,
        default=0
    )

    value = db.Column(
        db.Float,
        default=0
    )

    remarks = db.Column(
        db.String(250)
    )

    item = db.relationship(
        "ItemMaster"
    )

    job_work_detail = db.relationship(
        "JobWorkDetail"
    )

# ============================================================
# LABOUR MODULE MODELS
# ============================================================

class LabourTypeMaster(db.Model):
    __tablename__ = "labour_type_master"

    id = db.Column(db.Integer, primary_key=True)
    type_code = db.Column(db.String(20), unique=True, nullable=False)
    type_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True)


class LabourContractorMaster(db.Model):
    __tablename__ = "labour_contractor_master"

    id = db.Column(db.Integer, primary_key=True)
    contractor_code = db.Column(db.String(20), unique=True, nullable=True)
    contractor_name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(100))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(100))
    gst_no = db.Column(db.String(30))
    pan_no = db.Column(db.String(20))
    address = db.Column(db.String(500))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)

    labours = db.relationship("LabourMaster", backref="contractor", lazy=True)


class LabourMaster(db.Model):
    __tablename__ = "labour_master"

    id = db.Column(db.Integer, primary_key=True)
    labour_code = db.Column(db.String(20), unique=True, nullable=True)
    labour_name = db.Column(db.String(200), nullable=False)
    father_name = db.Column(db.String(200))
    gender = db.Column(db.String(10))  # Male / Female / Other
    date_of_birth = db.Column(db.Date)
    age = db.Column(db.Integer)
    blood_group = db.Column(db.String(10))
    aadhar_no = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    address = db.Column(db.String(500))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))

    # Work Details
    labour_type_id = db.Column(db.Integer, db.ForeignKey("labour_type_master.id"), nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey("labour_contractor_master.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location_master.id"), nullable=False)

    # Rate Details
    wage_type = db.Column(db.String(20), nullable=False, default="DAILY")
    # DAILY = Daily wages
    # PIECE = Piece rate

    daily_wage_rate = db.Column(db.Float, default=0)
    # For piece rate - rate is stored in ItemMaster.piece_rate

    # For contractors who pay labour, we track what we pay contractor
    contractor_rate = db.Column(db.Float, default=0)

    active = db.Column(db.Boolean, default=True)

    labour_type = db.relationship("LabourTypeMaster")
    location = db.relationship("LocationMaster")

    # Add piece_rate to ItemMaster - we'll handle this via migration


class LabourDailySheetHeader(db.Model):
    __tablename__ = "labour_daily_sheet_header"

    id = db.Column(db.Integer, primary_key=True)
    sheet_no = db.Column(db.String(30), unique=True, nullable=False)
    sheet_date = db.Column(db.Date, nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey("labour_contractor_master.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location_master.id"), nullable=False)
    remarks = db.Column(db.String(500))
    status = db.Column(db.String(20), default="DRAFT")  # DRAFT, APPROVED

    contractor = db.relationship("LabourContractorMaster")
    location = db.relationship("LocationMaster")
    entries = db.relationship("LabourDailySheetEntry", backref="sheet", cascade="all, delete-orphan")


class LabourDailySheetEntry(db.Model):
    __tablename__ = "labour_daily_sheet_entry"

    id = db.Column(db.Integer, primary_key=True)
    sheet_id = db.Column(db.Integer, db.ForeignKey("labour_daily_sheet_header.id"), nullable=False)
    labour_id = db.Column(db.Integer, db.ForeignKey("labour_master.id"), nullable=False)
    labour_type_id = db.Column(db.Integer, db.ForeignKey("labour_type_master.id"), nullable=False)

    # Time tracking
    time_in = db.Column(db.Time, nullable=False)
    time_out = db.Column(db.Time, nullable=False)
    break_hours = db.Column(db.Float, default=0)  # Lunch break in hours
    total_hours = db.Column(db.Float, default=0)  # Auto calculated

    # Production tracking - can have multiple items
    # This is stored in LabourDailySheetEntryDetail

    # Wage calculation
    wage_type = db.Column(db.String(20), nullable=False)  # DAILY or PIECE
    daily_rate = db.Column(db.Float, default=0)
    total_wages = db.Column(db.Float, default=0)

    labour = db.relationship("LabourMaster")
    labour_type = db.relationship("LabourTypeMaster")
    details = db.relationship("LabourDailySheetEntryDetail", backref="entry", cascade="all, delete-orphan")


class LabourDailySheetEntryDetail(db.Model):
    __tablename__ = "labour_daily_sheet_entry_detail"

    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("labour_daily_sheet_entry.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item_master.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe_header.id"), nullable=True)

    # Time on this item
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    hours_worked = db.Column(db.Float, default=0)  # Auto calculated

    # Production quantity
    qty_produced = db.Column(db.Float, default=0)

    # For piece rate
    piece_rate = db.Column(db.Float, default=0)
    piece_wages = db.Column(db.Float, default=0)

    # For daily wage - proportionate wages
    proportionate_wages = db.Column(db.Float, default=0)

    item = db.relationship("ItemMaster")
    recipe = db.relationship("RecipeHeader")

