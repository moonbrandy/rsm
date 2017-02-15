'''
Created on 17/11/2016

@author: Danny
'''
from __future__ import (absolute_import, unicode_literals, division,
                        print_function)

import os
import csv
import datetime

from django.db.transaction import atomic

from django.utils.six.moves import xrange 

from . import models

def na_to_none(d):
    if not d == "NA":
        return d
    else:
        return None

@atomic
def import_clientname_file(filename):
    '''Import client name from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'clientid'):
                print(row)
                models.ClientName.objects.create(
                    clientid=int(row[1]),
                    name=row[2],
                    legal_order=row[3],
                    address1=row[4],
                    address2=row[5],
                    address3=row[6]
                    )

@atomic
def import_licencetype_file(filename):
    '''Import licence type from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'licencetypeid'):
                print(row)
                models.LicenceType.objects.create(
                    licencetypeid=int(row[1]),
                    licencetypeidentifier=row[2],
                    workingdescription=row[3]
                    )

@atomic
def import_issuingoffice_file(filename):
    '''Import issuing office from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'officeid'):
                print(row)
                created = models.IssuingOffice.objects.create(
                    officeid=int(row[1]),
                    officecode=row[2],
                    officename=row[3]
                    )

@atomic
def import_managementright_file(filename):
    '''Import management right from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'managementrightid'):
                print(row)
                try:
                    client_id = models.ClientName.objects.get(clientid=row[2])
                    models.ManagementRight.objects.create(
                        managementrightid=row[1],
                        clientid=client_id,
                        mrcommencementdate=datetime.datetime.strptime(row[3], '%Y-%m-%d'),
                        mrregistrationdate=datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S'),
                        mrexpirydate=datetime.datetime.strptime(row[5], '%Y-%m-%d'),
                        mrconditions=row[6]
                    )
                except models.ClientName.DoesNotExist:
                    continue

@atomic
def import_licence_file(filename):
    '''Import licence from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'licenceid'):
                print(row)

                try:
                    client_name = models.ClientName.objects.get(clientid=int(row[3]))

                    if not row[2] == "NA":
                        try:
                            m_id = models.ManagementRight.objects.get(managementrightid=int(row[2]))
                        except models.ManagementRight.DoesNotExist:
                            m_id = None
                            print("NOT MATCHING MANAGEMENT RIGHT!!")
                            continue
                    else:
                        m_id = None

                    if not row[11] == "NA":
                        com_date = datetime.datetime.strptime(row[11], '%Y-%m-%d %H:%M:%S')
                    else:
                        com_date = None

                    if not row[12] == "NA":
                        reg_date = datetime.datetime.strptime(row[12], '%Y-%m-%d %H:%M:%S')
                    else:
                        reg_date = None

                    if not row[13] == "NA":
                        exp_date = datetime.datetime.strptime(row[13], '%Y-%m-%d')
                    else:
                        exp_date = None

                    if not row[10] == "NA":
                        licence_num = int(row[10])
                    else:
                        licence_num = None

                    licence_type = models.LicenceType.objects.get(licencetypeid=int(row[4]))
                    office = models.IssuingOffice.objects.get(officeid=int(row[9]))
                    models.Licence.objects.create(
                        licenceid=int(row[1]),
                        managementrightid=m_id,
                        clientid=client_name,
                        licencetypeid=licence_type,
                        licencetype=row[5],
                        licencecode=row[6],
                        licencecategory=row[7],
                        licencestatusid=int(row[8]),
                        officeid=office,
                        licencenumber=licence_num,
                        commencementdate=com_date,
                        registrationdate=reg_date,
                        expiry_date=exp_date,
                        sets=na_to_none(row[14]),
                        callsign=na_to_none(row[15]),
                        renewalfee=na_to_none(row[16]),
                        shipname=na_to_none(row[17]),
                        )
                except models.ClientName.DoesNotExist:
                    print("NOT MATCHING CLIENTNAME!!")
                    continue

                    

@atomic
def import_licenceconditions_file(filename):
    '''Import licence conditions from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'licenceid'):
                print(row)
                try:
                    licence = models.Licence.objects.get(licenceid=int(row[1]))
                    models.LicenceConditions.objects.create(
                        licenceid=licence,
                        licenceconditions=row[2],
                    )
                except models.Licence.DoesNotExist:
                    print("Not licence matching!!")
                    continue
                

@atomic
def import_radiationpattern_file(filename):
    '''Import radiation pattern from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'licenceid'):
                print(row)
                try:
                    licence = models.Licence.objects.get(licenceid=int(row[1]))
                    models.RadiationPattern.objects.create(
                        licenceid=licence,
                        patterntypeid=row[2],
                        bearingfrom=row[3],
                        bearingto=row[4],
                        bearingvalue=row[5],
                    )
                except models.Licence.DoesNotExist:
                    continue

@atomic
def import_mapdistrict_file(filename):
    '''Import map district from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'mapdistrictid'):
                print(row)
                models.MapDistrict.objects.create(
                    mapdistrictid=row[1],
                    mapcode=row[2],
                    district=row[3],
                    )

@atomic
def import_location_file(filename):
    '''Import location from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'locationid'):
                print(row)
                if not row[9] == "NA":
                    map_district = models.MapDistrict.objects.get(mapdistrictid=int(row[9]))
                else:
                    map_district = None
                models.Location.objects.create(
                    locationid=row[1],
                    districtid=map_district,
                    locationtypeid=row[2],
                    locationname=row[3],
                    locationheight=na_to_none(row[4]),
                    nominalmap=na_to_none(row[5]),
                    nominalref=na_to_none(row[6]),
                    longeast=na_to_none(row[7]),
                    longnorth=na_to_none(row[8]),
                    )

@atomic
def import_transmitconfiguration_file(filename):
    '''Import transmit configuration from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'transmitconfigurationid'):
                print(row)
                try:
                    licence = models.Licence.objects.get(licenceid=int(row[2]))
                    models.TransmitConfiguration.objects.create(
                        transmitconfigurationid=row[1],
                        licenceid=licence,
                        locationid=models.Location.objects.get(locationid=int(row[3])),
                        txantennamake=na_to_none(row[4]),
                        txantennatype=na_to_none(row[5]),
                        txantennaheight=na_to_none(row[6]),
                        txazimuth=na_to_none(row[7]),
                        txequipment=na_to_none(row[8]),
                    )
                except models.Licence.DoesNotExist:
                    print("Licence not matching!!")
                    continue

@atomic
def import_receiveconfiguration_file(filename):
    '''Import receive configuration from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'receiveconfigurationid'):
                print(row)
                try:
                    licence = models.Licence.objects.get(licenceid=int(row[2]))
                    models.ReceiveConfiguration.objects.create(
                        receiveconfigurationid=row[1],
                        licenceid=licence,
                        locationid=models.Location.objects.get(locationid=int(row[3])),
                        rxantennamake=na_to_none(row[4]),
                        rxantennatype=na_to_none(row[5]),
                        rxantennaheight=na_to_none(row[6]),
                        rxazimuth=na_to_none(row[7]),
                        rxequipment=na_to_none(row[8]),
                        mpis=na_to_none(row[9]),
                        mpisunit=na_to_none(row[10]),
                        wantedsignal=na_to_none(row[11]),
                        wantedunit=na_to_none(row[12]),
                    )
                except models.Licence.DoesNotExist:
                    print("Licence not matching for receiveconfiguration!!")
                    continue


@atomic
def import_associatedlicences_file(filename):
    '''Import associated licence from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'primarylicence'):
                print(row)
                try:
                    p_licence = models.Licence.objects.get(licenceid=row[1])
                    s_licence = models.Licence.objects.get(licenceid=row[2])
                    models.AssociatedLicences.objects.create(
                        primarylicence=p_licence,
                        associatedlicence=s_licence,
                        )
                except models.Licence.DoesNotExist:
                    print("Licence not exist!!")
                    continue

@atomic
def import_geographicreference_file(filename):
    '''Import geographic reference from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'locationid'):
                print(row)
                models.GeographicReference.objects.create(
                    locationid=models.Location.objects.get(locationid=int(row[1])),
                    georeferencetypeid=row[2],
                    georeferencetype=row[3],
                    easting=row[4],
                    northing=row[5],
                    mapnumber=na_to_none(row[6]),
                    original=row[7],
                    referenceorder=row[8],
                    )

@atomic
def import_emission_file(filename):
    '''Import emission from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'emissionid'):
                print(row)
                models.Emission.objects.update_or_create(
                    emissionid=int(row[1]),
                    defaults={"emission":row[2]},
                    )

@atomic
def import_spectrum_file(filename):
    '''Import spectrum from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'spectrumid'):
                print(row)
                if not row[17] == "NA":
                    start_date = datetime.datetime.strptime(row[17], '%Y-%m-%d %H:%M:%S')
                else:
                    start_date = None
                if not row[18] == "NA":
                    end_date = datetime.datetime.strptime(row[18], '%Y-%m-%d %H:%M:%S')
                else:
                    end_date = None
                if not row[19] == "NA":
                    regi_date = datetime.datetime.strptime(row[19], '%Y-%m-%d %H:%M:%S')
                else:
                    regi_date = None

                if not row[7] == "NA":
                    try:
                        licence = models.Licence.objects.get(licenceid=int(row[7]))
                    except models.Licence.DoesNotExist:
                        print("Licence cannot be found!!")
                        licence = None
                        pass
                else:
                    licence = None
                if not row[8] == "NA":
                    try:
                        mr = models.ManagementRight.objects.get(managementrightid=int(row[8]))
                    except models.ManagementRight.DoesNotExist:
                        print("MR cannot be found!!")
                        mr = None
                        pass
                else:
                    mr = None

                if not row[9] == "NA":
                    try:
                        emission = models.Emission.objects.get(emissionid=int(row[9]))
                    except models.Emission.DoesNotExist:
                        print("Emission ID does not exist!!")
                        emission = None
                else:
                    emission = None

                models.Spectrum.objects.update_or_create(
                    spectrumid=row[1],
                    defaults={
                    "spectrumstatusid":row[2],
                    "spectrumstatus":row[3],
                    "spectrumlabel":row[4],
                    "spectrumlow":row[5],
                    "spectrumhigh":row[6],
                    "licenceid":licence,
                    "managementrightid":mr,
                    "emissionid":emission,
                    "frequency":na_to_none(row[10]),
                    "power":na_to_none(row[11]),
                    "polarisation":row[12],
                    "polarisationcode":row[13],
                    "serviceid":row[14],
                    "spectrumtypeid":row[15],
                    "spectrumtype":row[16],
                    "startdate":start_date,
                    "enddate":end_date,
                    "registereddate":regi_date,
                    "spectrumremarks":na_to_none(row[20]),
                    },
                )

@atomic
def import_emissionlimit_file(filename):
    '''Import emission limit from csv to database
    '''
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=str(','), quotechar=str('\"'))
        for row in csv_reader:
            if not (row[1] == 'emissionlimitid'):
                print(row)
                try:
                    spectrum = models.Spectrum.objects.get(spectrumid=int(row[2]))
                    models.EmissionLimit.objects.create(
                        emissionlimitid=row[1],
                        spectrumid=spectrum,
                        emissionlimittypeid=row[3],
                        limitfrequency=row[4],
                        limitvalue=row[5],
                        limitgraphpoint=row[6],
                    )
                except models.Spectrum.DoesNotExist:
                    print("Cannot match spectrum!!")
                    continue
                

def import_all_files(directory):

    clientname_file = directory + 'clientname.csv'
    models.ClientName.objects.all().delete()
    import_clientname_file(clientname_file)

    licencetype_file = directory + 'licencetype.csv'
    models.LicenceType.objects.all().delete()
    import_licencetype_file(licencetype_file)

    issuingoffice_file = directory + 'issuingoffice.csv'
    models.IssuingOffice.objects.all().delete()
    import_issuingoffice_file(issuingoffice_file)

    managementright_file = directory + 'managementright.csv'
    models.ManagementRight.objects.all().delete()
    import_managementright_file(managementright_file)
    
    licence_file = directory + 'licence.csv'
    models.Licence.objects.all().delete()
    import_licence_file(licence_file)

    licenceconditions_file = directory + 'licenceconditions.csv'
    models.LicenceConditions.objects.all().delete()
    import_licenceconditions_file(licenceconditions_file)

    radiationpattern_file = directory + 'radiationpattern.csv'
    models.RadiationPattern.objects.all().delete()
    import_radiationpattern_file(radiationpattern_file)

    mapdistrict_file = directory + 'mapdistrict.csv'
    models.MapDistrict.objects.all().delete()
    import_mapdistrict_file(mapdistrict_file)
    
    location_file = directory + 'location.csv'
    models.Location.objects.all().delete()
    import_location_file(location_file)

    transmitconfiguration_file = directory + 'transmitconfiguration.csv'
    models.TransmitConfiguration.objects.all().delete()
    import_transmitconfiguration_file(transmitconfiguration_file)

    receiveconfiguration_file = directory + 'receiveconfiguration.csv'
    models.ReceiveConfiguration.objects.all().delete()
    import_receiveconfiguration_file(receiveconfiguration_file)

    associatedlicences_file = directory + 'associatedlicences.csv'
    models.AssociatedLicences.objects.all().delete()
    import_associatedlicences_file(associatedlicences_file)

    geographicreference_file = directory + 'geographicreference.csv'
    models.GeographicReference.objects.all().delete()
    import_geographicreference_file(geographicreference_file)

    emission_file = directory + 'emission.csv'
    models.Emission.objects.all().delete()
    import_emission_file(emission_file)

    spectrum_file = directory + 'spectrum.csv'
    models.Spectrum.objects.all().delete()
    import_spectrum_file(spectrum_file)

    emissionlimit_file = directory + 'emissionlimit.csv'
    models.EmissionLimit.objects.all().delete()
    import_emissionlimit_file(emissionlimit_file)
