"""
Ok, this should 
"""
from django_roa import Model as RoaModel
from django.db  import models 


class Organism(RoaModel):
    name = models.CharField(max_length=255,  unique=True) 
    hide_in_excel = models.BooleanField(default=False)
    other_information = models.CharField(max_length=255 , blank=True , null=True)
    def __unicode__(self) :
        return self.name
    class Meta:
        ordering = ['name']


class Project(RoaModel):
    name = models.CharField(max_length=30 , db_index=True , unique=True) 
    short_description = models.TextField(blank=True, null=True)
    other_info = models.TextField(null=True , blank=True)    

    def __unicode__(self) :
        return self.name
    class Meta:
        ordering = ['name']


class LabCenter(RoaModel):
    name = models.CharField(max_length=255, unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']



class SampleType(RoaModel):
    name = models.CharField(max_length=255, blank=True , null=True) 
    prepared_library = models.BooleanField(default=False)
    has_qc = models.BooleanField(default=True)
    display_order = models.IntegerField(null=True, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=['prepared_library', 'name']



class SampleStage(RoaModel):
    name = models.CharField(max_length=300) 
    def __unicode__(self) :
        return self.name
    class Meta:
        ordering = ['name']


class Cohort(RoaModel):
    name = models.CharField(max_length=255 , unique=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']



class Condition(RoaModel):
    condition = models.CharField(max_length=255 , unique=True)
    def __unicode__(self):
        return self.condition
    class Meta:
        ordering = ['condition']
        verbose_name_plural = "Sample status"


class ExpectedSample(RoaModel):
    """
    This will represent a sample for a collaborator to fill in. 
    """
    barcode = models.CharField(max_length=200 , unique=True) 
    name = models.CharField(max_length=90, null=True, blank=True , db_index=True) 

#    cnag_sample = models.NullBooleanField(default=False, verbose_name="Sample present at CNAG")   ### We have the sample here at cnag  (unlike received libraries)
    expected_insert_size =  models.CharField(max_length=255, null=True , blank=True) ## for chip seq samles

    project = models.ForeignKey(Project, db_index=True, ) ## not sure I need this here.  Depreciate this. 

    organism = models.ForeignKey(Organism,  null=True , blank=True , db_index=True )
    labcenter = models.ForeignKey(LabCenter , blank=True, null=True) #  this should be linked through project, or maybe not.....
    date_received = models.DateField(null=True, db_index=True , verbose_name="Sample received date") 
    
    comments = models.CharField(max_length=255 , null=True, blank=True) 
    sample_stage = models.ForeignKey(SampleStage , null=True, blank=True , verbose_name="Status") ## 'cos Matt can't make up his mind what to call columns. "Stage", "no change it to status", "no stage, ....."
    lab_book_page = models.CharField(max_length=120, null=True,  blank=True) 
    nanodrop_sample = models.DecimalField(decimal_places=2, null=True, max_digits=7, blank=True) 
    nanodrop_lib = models.DecimalField(decimal_places=2, null=True, max_digits=7, blank=True) 
    picogreen_lib = models.DecimalField(decimal_places=2, null=True, max_digits=7, blank=True) 
    picogreen_sample = models.DecimalField(decimal_places=2, null=True, max_digits=7, blank=True) 
    qpcr = models.DecimalField(decimal_places=2, null=True, max_digits=7, blank=True) 
    final_concentration_lib = models.DecimalField(decimal_places=2, null=True, max_digits=7, blank=True) 
    invoice_number = models.CharField(max_length=120, blank=True , null=True) 
    project_number = models.CharField(max_length=120, blank=True , null=True) 
    order_number = models.IntegerField(null=True, blank=True) 
    titration_lib = models.DecimalField(decimal_places=2, null=True, max_digits=7, blank=True) 
    ribogreen_lib = models.DecimalField(decimal_places=2, null=True, max_digits=7, blank=True) 
    cohort = models.ForeignKey(Cohort , null=True, blank=True , db_index=True)  
    # new fields
    material_type = models.CharField(max_length=255, blank=True , null=True , verbose_name="material type (use sample type instead)")
    material_source = models.CharField(max_length=255, blank=True , null=True)
    extraction_method = models.CharField(max_length=255, blank=True, null=True)
    initial_volume = models.DecimalField(max_digits=7, decimal_places=3  ,  null=True, blank=True)
    buffer = models.CharField(max_length=255, blank=True , null=True)
    quantification_method = models.CharField(max_length=255, blank=True , null=True)
    
    reported_concentration = models.DecimalField(max_digits=7, decimal_places=3 , null=True, blank=True)
    absorbance_ratio_260_280 = models.DecimalField(max_digits=7, decimal_places=3 , null=True, blank=True)
    absorbance_ratio_260_230 = models.DecimalField(max_digits=7, decimal_places=3 , null=True, blank=True)
    
    sex = models.CharField(max_length=20  , blank=True , null=True)   ## male = 1, 1.0 , 2, 2.0 = female
    condition = models.ForeignKey(Condition, blank=True, null=True) ; 
    pedigree = models.CharField(max_length=256 , blank=True, null=True)
    father_id = models.CharField( max_length=40,null=True,  blank =True)
    mother_id = models.CharField( max_length=40,null=True,  blank =True)    
    geographic_origin = models.TextField(blank=True , null=True)
    
    replacement = models.BooleanField(default=False)
    replacement_for = models.ForeignKey('self', null=True, blank=True)
    other_import_information = models.TextField(null=True, blank=True)
    
    sample_type = models.ForeignKey(SampleType, blank=True, null=True , verbose_name='Collab. Sample Type')  ## want to use subproject.sample_type, BUT sometimes samples entered before subproject, so use this as a check


    def __unicode__(self):
        return self.barcode

    