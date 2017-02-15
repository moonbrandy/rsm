
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ClientName(models.Model):
    clientid = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    legal_order = models.IntegerField()
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    address3 = models.CharField(max_length=200)

    def __str__(self):
        return str(self.clientid)

@python_2_unicode_compatible
class IssuingOffice(models.Model):
    officeid = models.IntegerField(primary_key=True, editable=False)
    officecode = models.CharField(max_length=5)
    officename = models.CharField(max_length=50)

    def __str__(self):
        return str(self.officeid)

@python_2_unicode_compatible
class ManagementRight(models.Model):
    managementrightid = models.IntegerField(primary_key=True, editable=False)
    clientid = models.ForeignKey('ClientName', to_field='clientid')
    mrcommencementdate = models.DateTimeField()
    mrregistrationdate = models.DateTimeField()
    mrexpirydate = models.DateTimeField()
    mrconditions = models.CharField(max_length=5000)

    def __str__(self):
        return str(self.managementrightid)

@python_2_unicode_compatible
class LicenceType(models.Model):
    licencetypeid = models.IntegerField(primary_key=True, editable=False)
    licencetypeidentifier = models.CharField(max_length=5)
    workingdescription = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.licencetypeid)

@python_2_unicode_compatible
class Licence(models.Model):
    licenceid = models.IntegerField(primary_key=True, editable=False)
    clientid = models.ForeignKey('ClientName', to_field='clientid')
    officeid = models.ForeignKey('IssuingOffice', to_field='officeid')
    managementrightid = models.ForeignKey('ManagementRight', to_field='managementrightid',null=True,blank=True)
    licencetypeid = models.ForeignKey('LicenceType', to_field='licencetypeid')
    licencetype = models.CharField(max_length=200)
    licencecode = models.CharField(max_length=5)
    licencecategory = models.CharField(max_length=50)
    licencestatusid = models.IntegerField()
    licencenumber = models.IntegerField(null=True,blank=True)
    commencementdate = models.DateTimeField(null=True,blank=True)
    registrationdate = models.DateTimeField(null=True,blank=True)
    expiry_date = models.DateTimeField(null=True,blank=True)
    sets = models.IntegerField(null=True,blank=True)
    callsign = models.CharField(max_length=10,null=True,blank=True)
    renewalfee = models.IntegerField(null=True,blank=True)
    shipname = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.licenceid)

@python_2_unicode_compatible
class LicenceConditions(models.Model):
    licenceid = models.ForeignKey('Licence', to_field='licenceid')
    licenceconditions = models.CharField(max_length=10000)

    def __str__(self):
        return str(self.id)

@python_2_unicode_compatible
class RadiationPattern(models.Model):
    licenceid = models.ForeignKey('Licence', to_field='licenceid')
    patterntypeid = models.IntegerField()
    bearingfrom = models.FloatField()
    bearingto = models.FloatField()
    bearingvalue = models.FloatField()

    def __str__(self):
        return str(self.id)

@python_2_unicode_compatible
class Emission(models.Model):
    emissionid = models.IntegerField(primary_key=True, editable=False)
    emission = models.CharField(max_length=20)

    def __str__(self):
        return str(self.emissionid)

@python_2_unicode_compatible
class AssociatedLicences(models.Model):
    primarylicence = models.ForeignKey('Licence', to_field='licenceid', related_name='primarylicence')
    associatedlicence = models.ForeignKey('Licence', to_field='licenceid', related_name='associatedlicence')

    def __str__(self):
        return str(self.id)

@python_2_unicode_compatible
class MapDistrict(models.Model):
    mapdistrictid = models.IntegerField(primary_key=True, editable=False)
    mapcode = models.CharField(max_length=10)
    district = models.CharField(max_length=10)

    def __str__(self):
        return str(self.mapdistrictid)

@python_2_unicode_compatible
class Location(models.Model):
    locationid = models.IntegerField(primary_key=True, editable=False)
    districtid = models.ForeignKey('MapDistrict', to_field='mapdistrictid',null=True,blank=True)
    locationtypeid = models.IntegerField()
    locationname = models.CharField(max_length=200)
    locationheight = models.IntegerField(null=True,blank=True)
    nominalmap = models.CharField(max_length=5,null=True,blank=True)
    nominalref = models.IntegerField(null=True,blank=True)
    longeast = models.IntegerField(null=True,blank=True)
    longnorth = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.locationid)

@python_2_unicode_compatible
class Spectrum(models.Model):
    spectrumid = models.IntegerField(primary_key=True, editable=False)
    licenceid = models.ForeignKey('Licence', to_field='licenceid',null=True,blank=True)
    managementrightid = models.ForeignKey('ManagementRight', to_field='managementrightid',null=True,blank=True)
    emissionid = models.ForeignKey('Emission', to_field='emissionid',null=True,blank=True)
    spectrumstatusid = models.IntegerField()
    spectrumstatus = models.CharField(max_length=20)
    spectrumlabel = models.CharField(max_length=20,null=True,blank=True)
    spectrumlow = models.FloatField()
    spectrumhigh = models.FloatField()    
    frequency = models.FloatField(null=True,blank=True)
    power = models.FloatField(null=True,blank=True)
    polarisation = models.CharField(max_length=50)
    polarisationcode = models.CharField(max_length=5)
    serviceid = models.IntegerField()
    spectrumtypeid = models.IntegerField()
    spectrumtype = models.CharField(max_length=20)
    startdate = models.DateTimeField(null=True,blank=True)
    enddate = models.DateTimeField(null=True,blank=True)
    registereddate = models.DateTimeField(null=True,blank=True)
    spectrumremarks = models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return str(self.spectrumid)

@python_2_unicode_compatible
class EmissionLimit(models.Model):
    emissionlimitid = models.IntegerField(primary_key=True, editable=False)
    spectrumid = models.ForeignKey('Spectrum', to_field='spectrumid')
    emissionlimittypeid = models.IntegerField()
    limitfrequency = models.FloatField()
    limitvalue = models.FloatField()
    limitgraphpoint = models.CharField(max_length=5)

    def __str__(self):
        return str(self.emissionlimitid)

@python_2_unicode_compatible
class GeographicReference(models.Model):
    locationid = models.ForeignKey('Location', to_field='locationid')
    georeferencetypeid = models.IntegerField()
    georeferencetype = models.CharField(max_length=100)
    easting = models.FloatField()
    northing = models.FloatField()
    mapnumber = models.CharField(max_length=5,null=True,blank=True)
    original = models.CharField(max_length=5)
    referenceorder = models.IntegerField()

    def __str__(self):
        return str(self.id)

@python_2_unicode_compatible
class TransmitConfiguration(models.Model):
    transmitconfigurationid = models.IntegerField(primary_key=True, editable=False)
    licenceid = models.ForeignKey('Licence', to_field='licenceid')
    locationid = models.ForeignKey('Location', to_field='locationid')
    txantennamake = models.CharField(max_length=100,null=True,blank=True)
    txantennatype = models.CharField(max_length=100,null=True,blank=True)
    txantennaheight = models.IntegerField(null=True,blank=True)
    txazimuth = models.FloatField(null=True,blank=True)
    txequipment = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.transmitconfigurationid)

@python_2_unicode_compatible
class ReceiveConfiguration(models.Model):
    receiveconfigurationid = models.IntegerField(primary_key=True,editable=False)
    licenceid = models.ForeignKey('Licence', to_field='licenceid')
    locationid = models.ForeignKey('Location', to_field='locationid')
    rxantennamake = models.CharField(max_length=100,null=True,blank=True)
    rxantennatype = models.CharField(max_length=100,null=True,blank=True)
    rxantennaheight = models.IntegerField(null=True,blank=True)
    rxazimuth = models.FloatField(null=True,blank=True)
    rxequipment = models.CharField(max_length=100,null=True,blank=True)
    mpis = models.FloatField(null=True,blank=True)
    mpisunit = models.CharField(max_length=100,null=True,blank=True)
    wantedsignal = models.FloatField(null=True,blank=True)
    wantedunit = models.CharField(max_length=100,null=True,blank=True)

    def __str__(slef):
        return str(self.receiveconfigurationid)
