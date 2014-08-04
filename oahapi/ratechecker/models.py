from django.db import models

# I'm not fond of how these fields are named, but I tried to balance
# Python naming conventions with how the fields are actually referred to
# outside this software.


class Product(models.Model):
    """ Loan Product. """

    FIXED = 'FIXED'
    ARM = 'ARM'

    PAYMENT_TYPE_CHOICES = (
        (FIXED, 'Fixed Rate Mortgage'),
        (ARM, 'Adjustable Rate Mortgage'))

    JUMBO = 'JUMBO'
    CONF = 'CONF'
    AGENCY = 'AGENCY'
    FHA = 'FHA'
    VA = 'VA'
    VA_HB = 'VA-HB'
    FHA_HB = 'FHA-HB'

    LOAN_TYPE_CHOICES = (
        (JUMBO, 'Jumbo Mortgage'),
        (CONF, 'Conforming Loan'),
        (AGENCY, 'Agency Loan'),
        (FHA, 'Federal Housing Administration Loan'),
        (VA, 'Veterans Affairs Loan'),
        (VA_HB, 'VA-HB Loan'),
        (FHA_HB, 'FHA-HB Loan'),
    )

    REFI = 'REFI'
    PURCH = 'PURCH'

    LOAN_PURPOSE_CHOICES = (
        (REFI, 'Refinance'),
        (PURCH, 'Purchase')
    )

    plan_id = models.IntegerField(primary_key=True)
    institution = models.CharField(max_length=16)
    loan_purpose = models.CharField(
        max_length=12, choices=LOAN_PURPOSE_CHOICES)
    pmt_type = models.CharField(
        max_length=12, choices=PAYMENT_TYPE_CHOICES, default=FIXED)
    loan_type = models.CharField(max_length=12, choices=LOAN_TYPE_CHOICES)
    loan_term = models.IntegerField()
    int_adj_term = models.IntegerField(
        null=True,
        help_text='1st part of the ARM definition. E.g. 5 in 5/1 ARM')
    adj_period = models.PositiveSmallIntegerField(null=True)
    io = models.BooleanField()
    arm_index = models.CharField(max_length=96, null=True)

    iac_help = 'Max percentage points the rate can adjust at first adjustment.'
    int_adj_cap = models.IntegerField(null=True, help_text=iac_help)

    cap_text = 'Max percentage points adjustable at each subsequent adjustment'
    annual_cap = models.IntegerField(null=True, help_text=cap_text)

    loan_cap = models.IntegerField(
        null=True,
        help_text='Total lifetime maximum change that the ARM rate can have.')
    arm_margin = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    ai_value = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    min_ltv = models.FloatField()
    max_ltv = models.FloatField()
    min_fico = models.IntegerField()
    max_fico = models.IntegerField()
    min_loan_amt = models.DecimalField(max_digits=12, decimal_places=2)
    max_loan_amt = models.DecimalField(max_digits=12, decimal_places=2)
    singlefamily = models.BooleanField()
    condo = models.BooleanField()
    coop = models.BooleanField()


class Adjustment(models.Model):

    POINTS = 'P'
    RATE = 'R'

    AFFECT_RATE_TYPE_CHOICES = (
        (POINTS, 'Points'),
        (RATE, 'Rate'))

    rule_id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product)
    affect_rate_type = models.CharField(
        max_length=1, choices=AFFECT_RATE_TYPE_CHOICES)
    adj_value = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    min_loan_amt = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    max_loan_amt = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    prop_type = models.CharField(max_length=10, null=True)
    min_fico = models.IntegerField(null=True)
    max_fico = models.IntegerField(null=True)
    min_ltv = models.FloatField(null=True)
    max_ltv = models.FloatField(null=True)
    state = models.CharField(max_length=2, null=True)


class Region(models.Model):
    """ This table maps regions to states. """
    region_id = models.IntegerField()
    state_id = models.CharField(max_length=2)


class Rate(models.Model):
    rates_id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product)
    regions = models.ManyToManyField(Region)
    lock = models.PositiveSmallIntegerField()
    base_rate = models.DecimalField(max_digits=6, decimal_places=3)
    total_points = models.DecimalField(max_digits=6, decimal_places=3)
