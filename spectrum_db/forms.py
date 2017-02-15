from dal import autocomplete

from django import forms

from datetimewidget.widgets import DateWidget

class NoValidationSelect2List(autocomplete.Select2ListChoiceField):
    def __init__(self, *args, **kwargs):
        super(NoValidationSelect2List, self).__init__(*args, **kwargs)

    def validate(self, value):
        # skip validation
        pass

class SearchLicenceForm(forms.Form):
    '''form that used for search licences'''
    CERTIFIED_BY_OPTIONS = (
        ("","Any"),
        (61,"ADAM CHARLES TOMMY"),
        (101,"ALAN JOHN WALLACE"),
        (15,"ALAN MICHAEL TURNER"),
        (21,"ALAN ROSS JAMIESON"),
        (42,"ALEC OLEH DEMETRIUS KRECHOWEC"),
        (157,"Alex  Ho Cheong Wong"),
        (36,"Alex Orange"),
        (108,"Alexander Peter TOLLENAAR"),
        (173,"Allan Royden Gray"),
        (163,"ALLAN STANLEY WARD"),
        (81,"ALLISTER MCKENZIE BABINGTON"),
        (54,"ANDREW BARRON"),
        (92,"ANDREW JAMES SMITHIES"),
        (121,"ANDREW JOHN MAY"),
        (35,"ANTHONY DOUGLAS BROWN"),
        (170,"Arasaratnam Sathyendran"),
        (175,"Bede Patrick McCormick"),
        (174,"Belen Andres-Garcia"),
        (51,"BILL JACOB"),
        (45,"BRENT JONES"),
        (120,"BRENT MARK JAGUSCH"),
        (135,"Brett Alan Shaw"),
        (69,"BRIAN DAVIS"),
        (49,"BRUCE DOUGLAS HARDING"),
        (88,"BRYAN KENNETH McCONACHIE"),
        (150,"C Rod Heazlewood"),
        (165,"Chap Micua"),
        (76,"CHARLES MCMILLAN"),
        (109,"CHESTER  P N CLARK"),
        (172,"Chris Zawodny"),
        (178,"Christopher John Thomson"),
        (73,"CRAIG ANDREW SCOTT"),
        (86,"CRAWFORD ANDREW BAIRD"),
        (123,"CRISTIAN GOMEZ"),
        (22,"D KERSHAW"),
        (19,"DARREN FRASER CHEW"),
        (138,"Dave E Lord"),
        (106,"DAVID ARTHUR JOHN THOMSON"),
        (134,"DAVID HARTON"),
        (87,"DAVID JOHN CROOK"),
        (141,"David John Neil"),
        (85,"DAVID JOHN TAYLOR"),
        (89,"DAVID PATRICK ADAMSON"),
        (31,"DAVID ROBINSON"),
        (72,"DAVID WALKER"),
        (179,"David Wall"),
        (59,"DIGBY CLYDE GUDSELL"),
        (78,"EEMAN EMMANUEL YAQUB"),
        (65,"EION NEIL GIBSON"),
        (105,"ERIC DEAN GEORGE SMITH"),
        (132,"ERIC ENRIQUEZ IBANEZ"),
        (177,"Eric George Jones"),
        (83,"ERIC YUAN LIU"),
        (131,"Ernest Hong"),
        (151,"Farouk Sulaman"),
        (133,"GARETH J BENNETT"),
        (57,"GARRY KENNETH RODGERS"),
        (124,"GARTH CHRISTOPHER SPENCER"),
        (50,"GAVIN CUMMERFIELD"),
        (58,"GEOFFREY DAVID COLLINS"),
        (39,"GEOFFREY PHILIP COLE"),
        (84,"GEOFFREY WILLIAM TUNNICLIFFE"),
        (1,"GEORGE HUGH RAILTON"),
        (60,"GRAHAM FRANK HULSTON"),
        (136,"Grahame A LOVE"),
        (144,"Grant Joseph Crombie"),
        (99,"GREGORY JOHN WALSH"),
        (33,"GREGORY MARK FOWLIE"),
        (107,"GREGORY SMITH"),
        (48,"IAN BAYNE MACDONALD"),
        (122,"IAN DAVID TIMEWELL"),
        (53,"IAN GILLESPIE"),
        (30,"Ian Goodwin"),
        (181,"Ian Graham"),
        (113,"Ian Harris"),
        (23,"Ian Rex Hutchings"),
        (62,"JAMES DANIEL WINDSOR"),
        (169,"Jangez Khan"),
        (95,"JASON LEIF HEALEY"),
        (145,"Jason R Hills"),
        (97,"JEFFERY BURGESS SAYER"),
        (47,"JEFFREY DENNIS HICKS"),
        (24,"JENIFER MUNDY"),
        (158,"John Douglas Chisholm"),
        (38,"JOHN DOUGLAS INGHAM"),
        (171,"John Hodren"),
        (154,"John Michael Challinor"),
        (80,"John S C Yaldwyn"),
        (168,"Johnathon Green"),
        (159,"Jonathan Michael Brewer"),
        (115,"JOSEPH M G DEN EXTER"),
        (182,"Justin Wonderlick"),
        (160,"Keith A RAMSAY"),
        (130,"KEITH DESMOND SALTER"),
        (162,"Keith Frederick Lantsbury"),
        (77,"KEVIN DOVE"),
        (140,"L G BARKER"),
        (11,"Larry (HILARY JOHN) PURCHAS"),
        (102,"LAURANCE JAMES COLVIN"),
        (164,"Leslie John Cole"),
        (161,"Malcolm David Wallace"),
        (17,"MANSOOR SHAFI"),
        (156,"Mervyn Frericks"),
        (75,"MICHAEL COOKE-RUSSELL"),
        (20,"Michael John Lancaster"),
        (26,"MICHAEL WILLIAM HOULIHAN"),
        (176,"Mircea Andrei Stoian"),
        (116,"NEIL HARRY LAMBERT"),
        (117,"NEILL MARTIN ELLIS"),
        (70,"NEVILLE HENRY"),
        (90,"NICHOLAS LLOYD WENSLEY"),
        (129,"NIGEL BARRIE CRABBE"),
        (139,"Paul Kearney"),
        (64,"PETER ANDREW CASEY"),
        (180,"Peter Gent"),
        (5,"PETER HAYES MCFARLANE"),
        (68,"PETER HILLY"),
        (118,"PETER R MOORE"),
        (104,"PHILIP JOHN BLACK"),
        (63,"PHILLIP JOHN BRIESEMAN"),
        (56,"PHILLIP LYLE JOHNSTON"),
        (127,"REX HARRIS"),
        (9,"RICHARD BROWN"),
        (55,"RICHARD JOSEPH COLLINS"),
        (46,"Richard Sawers"),
        (146,"Robert A Halliday"),
        (7,"ROBERT BRIAN VERNALL"),
        (147,"Robert L Griffith"),
        (111,"ROBERT McCRAE"),
        (79,"ROGER MILES KIPPENBERGER"),
        (167,"Roger Noel Collinge"),
        (96,"ROLAND ROGER OSBORNE"),
        (37,"ROSS DOYLE COOPER"),
        (40,"ROSS MURDOCH"),
        (114,"ROSS TOTTENHAM"),
        (71,"RUSSELL BIRT"),
        (91,"RUSSELL JOHN WATSON"),
        (112,"RUSSELL W RICHARDSON"),
        (52,"SALVIN JOHN WILSON"),
        (137,"Scott G BILLINGTON"),
        (143,"Sean K CRAWFORD"),
        (148,"Shaun Godfrey"),
        (43,"SIEGMUND WIESER"),
        (25,"SIMON OLIVER COOKE-WILLIS"),
        (149,"Stephen Douglas Hooper"),
        (142,"Stephen F FOGERTY"),
        (152,"Stephen Michael Atkinson"),
        (100,"STEPHEN RICHARD OLDFIELD"),
        (125,"STEVEN PAUL GILLETT"),
        (98,"Stewart James Hall"),
        (74,"TERRENCE FAHEY"),
        (41,"Thaddeus David Julian"),
        (166,"Theresa Van Rooyen"),
        (29,"TREVOR GEORGE WOODS"),
        (82,"VERNON GEORGE TALBOT"),
        (155,"Vincent Agustin"),
        (153,"WARREN KYLE HARRIS"),
        (44,"WILHELMUS CORNELIS ZWART"),
        (94,"WILLIAM DOUGLAS WARRILOW"),
        (128,"WILLIAM HENRY WATERWORTH"),
        )

    LICENCE_TYPE_OPTIONS = (
        ("","Any"),
        ("Aero Base (Off Route)","Aero Base (Off Route)"),
        ("Aero Base (Route)","Aero Base (Route)"),
        ("Aero Mobile","Aero Mobile"),
        ("Aero Mobile (Off Route)","Aero Mobile (Off Route)"),
        ("Aero Mobile (Route)","Aero Mobile (Route)"),
        ("Aero Mobile - Mobile Transmit","Aero Mobile - Mobile Transmit"),
        ("Aero Repeater","Aero Repeater"),
        ("Aircraft","Aircraft"),
        ("Amateur Beacon","Amateur Beacon"),
        ("Amateur Digipeater","Amateur Digipeater"),
        ("Amateur Fixed","Amateur Fixed"),
        ("Amateur General","Amateur General"),
        ("Amateur Limited","Amateur Limited"),
        ("Amateur Limited/Novice","Amateur Limited/Novice"),
        ("Amateur Novice","Amateur Novice"),
        ("Amateur Repeater","Amateur Repeater"),
        ("Amateur Repeater - Mobile Transmit","Amateur Repeater - Mobile Transmit"),
        ("Amateur TV Repeater","Amateur TV Repeater"),
        ("Defence","Defence"),
        ("Fixed < 1GHz; BW <=12.5kHz (Bi-directional)","Fixed < 1GHz; BW <=12.5kHz (Bi-directional)"),
        ("Fixed < 1GHz; BW <=12.5kHz (Uni-directional)","Fixed < 1GHz; BW <=12.5kHz (Uni-directional)"),
        ("Fixed < 1GHz; BW >12.5kHz & <=50kHz (Bi-directional)","Fixed < 1GHz; BW >12.5kHz & <=50kHz (Bi-directional)"),
        ("Fixed < 1GHz; BW >12.5kHz & <=50kHz (Uni-directional)","Fixed < 1GHz; BW >12.5kHz & <=50kHz (Uni-directional)"),
        ("Fixed < 1GHz; BW >50kHz (Bi-directional)","Fixed < 1GHz; BW >50kHz (Bi-directional)"),
        ("Fixed < 1GHz; BW >50kHz (Uni-directional)","Fixed < 1GHz; BW >50kHz (Uni-directional)"),
        ("Fixed >=14GHz (Bi-directional)","Fixed >=14GHz (Bi-directional)"),
        ("Fixed >=14GHz (Uni-directional)","Fixed >=14GHz (Uni-directional)"),
        ("Fixed >=1GHz & <14GHz (Bi-directional)","Fixed >=1GHz & <14GHz (Bi-directional)"),
        ("Fixed >=1GHz & <14GHz (Uni-directional)","Fixed >=1GHz & <14GHz (Uni-directional)"),
        ("Fixed Bi-directional Point-to-Multipoint","Fixed Bi-directional Point-to-Multipoint"),
        ("Fixed Outside Broadcast O Band","Fixed Outside Broadcast O Band"),
        ("Fixed Outside Broadcast V Band","Fixed Outside Broadcast V Band"),
        ("Fixed Uni-directional Point-to-Multipoint","Fixed Uni-directional Point-to-Multipoint"),
        ("General user licence (Radio)","General user licence (Radio)"),
        ("General user licence (Spectrum)","General user licence (Spectrum)"),
        ("HF AM <30dBW (Radio)","HF AM <30dBW (Radio)"),
        ("HF AM >=30 & <36dBW (Radio)","HF AM >=30 & <36dBW (Radio)"),
        ("HF AM >=36 & <40dBW (Radio)","HF AM >=36 & <40dBW (Radio)"),
        ("HF AM >=40dBW (Radio)","HF AM >=40dBW (Radio)"),
        ("Land Mobile - Mobile Transmit","Land Mobile - Mobile Transmit"),
        ("Land Repeater <=5W; BW <=12.5kHz","Land Repeater <=5W; BW <=12.5kHz"),
        ("Land Repeater <=5W; BW >12.5kHz","Land Repeater <=5W; BW >12.5kHz"),
        ("Land Repeater >5W; BW <=12.5kHz","Land Repeater >5W; BW <=12.5kHz"),
        ("Land Repeater >5W; BW >12.5kHz","Land Repeater >5W; BW >12.5kHz"),
        ("Land Repeater NZ Wide; BW <=12.5kHz","Land Repeater NZ Wide; BW <=12.5kHz"),
        ("Land Repeater NZ Wide; BW >12.5kHz","Land Repeater NZ Wide; BW >12.5kHz"),
        ("Land Simplex","Land Simplex"),
        ("Land Simplex Govt. use only; BW <=12.5kHz","Land Simplex Govt. use only; BW <=12.5kHz"),
        ("Land Simplex Govt. use only; BW >12.5kHz & <=25kHz","Land Simplex Govt. use only; BW >12.5kHz & <=25kHz"),
        ("Land Simplex Govt. use only; BW >25kHz","Land Simplex Govt. use only; BW >25kHz"),
        ("Licence to Transmit only (Spectrum)","Licence to Transmit only (Spectrum)"),
        ("Licence to have no Interference (Spectrum)","Licence to have no Interference (Spectrum)"),
        ("MF AM <30dBW (Spectrum)","MF AM <30dBW (Spectrum)"),
        ("MF AM >=30 & <36dBW (Spectrum)","MF AM >=30 & <36dBW (Spectrum)"),
        ("MF AM >=36 & <40dBW (Spectrum)","MF AM >=36 & <40dBW (Spectrum)"),
        ("MF AM >=40dBW (Spectrum)","MF AM >=40dBW (Spectrum)"),
        ("Maritime Mobile","Maritime Mobile"),
        ("Maritime Mobile - Mobile Transmit","Maritime Mobile - Mobile Transmit"),
        ("Maritime Private Coast Station","Maritime Private Coast Station"),
        ("Maritime Public Coast Station","Maritime Public Coast Station"),
        ("Maritime Repeater","Maritime Repeater"),
        ("Meteorological Aid","Meteorological Aid"),
        ("Meteorological Radar","Meteorological Radar"),
        ("Other <10dBW (Spectrum)","Other <10dBW (Spectrum)"),
        ("Other >=10 & <20dBW (Spectrum)","Other >=10 & <20dBW (Spectrum)"),
        ("Other >=20 & <30dBW (Spectrum)","Other >=20 & <30dBW (Spectrum)"),
        ("Other >=30dBW (Spectrum)","Other >=30dBW (Spectrum)"),
        ("PRS Repeater","PRS Repeater"),
        ("Paging - NZ Wide","Paging - NZ Wide"),
        ("Paging <=5W","Paging <=5W"),
        ("Paging >25W","Paging >25W"),
        ("Paging >5W & <=25W","Paging >5W & <=25W"),
        ("Radio Det - Other than Met Service","Radio Det - Other than Met Service"),
        ("Radio Det - Two frequency","Radio Det - Two frequency"),
        ("Radiodet - Aero ILS","Radiodet - Aero ILS"),
        ("Radiodet - Radio Beacons (VOR, NDB)","Radiodet - Radio Beacons (VOR, NDB)"),
        ("Radiodet - Radionav (incl DME)","Radiodet - Radionav (incl DME)"),
        ("Radiodetermination - Mobile Transmit","Radiodetermination - Mobile Transmit"),
        ("Radiodetermination - Mobile Transmit","Radiodetermination - Mobile Transmit"),
        ("Sat Fixed Per Transponder","Sat Fixed Per Transponder"),
        ("Sat Receive Only","Sat Receive Only"),
        ("Satellite - Mobile","Satellite - Mobile"),
        ("Satellite - Satellite Transmit","Satellite - Satellite Transmit"),
        ("Satellite - VSAT Network","Satellite - VSAT Network"),
        ("Ship - 2182kHz Only","Ship - 2182kHz Only"),
        ("Ship - Compulsory Radiotelegraphy","Ship - Compulsory Radiotelegraphy"),
        ("Ship - Compulsory Radiotelephony","Ship - Compulsory Radiotelephony"),
        ("Ship - Voluntary","Ship - Voluntary"),
        ("Telemetry/Telecommand (Bi-directional)","Telemetry/Telecommand (Bi-directional)"),
        ("Telemetry/Telecommand (Uni-directional)","Telemetry/Telecommand (Uni-directional)"),
        ("UHF TV <10dBW (Radio)","UHF TV <10dBW (Radio)"),
        ("UHF TV <10dBW (Spectrum)","UHF TV <10dBW (Spectrum)"),
        ("UHF TV >=10 & <30dBW (Radio)","UHF TV >=10 & <30dBW (Radio)"),
        ("UHF TV >=10 & <30dBW (Spectrum)","UHF TV >=10 & <30dBW (Spectrum)"),
        ("UHF TV >=30 & <40dBW (Radio)","UHF TV >=30 & <40dBW (Radio)"),
        ("UHF TV >=30 & <40dBW (Spectrum)","UHF TV >=30 & <40dBW (Spectrum)"),
        ("UHF TV >=40 & <50dBW (Radio)","UHF TV >=40 & <50dBW (Radio)"),
        ("UHF TV >=40 & <50dBW (Spectrum)","UHF TV >=40 & <50dBW (Spectrum)"),
        ("UHF TV >=50dBW (Radio)","UHF TV >=50dBW (Radio)"),
        ("UHF TV >=50dBW (Spectrum)","UHF TV >=50dBW (Spectrum)"),
        ("VHF FM <10dBW (Radio)","VHF FM <10dBW (Radio)"),
        ("VHF FM <10dBW (Spectrum)","VHF FM <10dBW (Spectrum)"),
        ("VHF FM >=10 & <20dBW (Radio)","VHF FM >=10 & <20dBW (Radio)"),
        ("VHF FM >=10 & <20dBW (Spectrum)","VHF FM >=10 & <20dBW (Spectrum)"),
        ("VHF FM >=20 & <30dBW (Radio)","VHF FM >=20 & <30dBW (Radio)"),
        ("VHF FM >=20 & <30dBW (Spectrum)","VHF FM >=20 & <30dBW (Spectrum)"),
        ("VHF FM >=30 & <40dBW (Radio)","VHF FM >=30 & <40dBW (Radio)"),
        ("VHF FM >=30 & <40dBW (Spectrum)","VHF FM >=30 & <40dBW (Spectrum)"),
        ("VHF FM >=40dBW (Radio)","VHF FM >=40dBW (Radio)"),
        ("VHF FM >=40dBW (Spectrum)","VHF FM >=40dBW (Spectrum)"),
        ("VHF TV <10dBW (Spectrum)","VHF TV <10dBW (Spectrum)"),
        ("VHF TV >=10 & < 30dBW (Spectrum)","VHF TV >=10 & < 30dBW (Spectrum)"),
        ("VHF TV >=30 & <50dBW (Spectrum)","VHF TV >=30 & <50dBW (Spectrum)"),
        ("VHF TV >=50dBW (Spectrum)","VHF TV >=50dBW (Spectrum)"),
        )

    LICENCE_STATUS_OPTION = (
        ("ALL", "All Permissible"),
        ("CANCELLED_1", "Cancelled"),
        ("CERTIFICATE_EXPIRED_10", "Certificate Expired"),
        ("CURRENT_8", "Current"),
        ("CURRENT_AND_PLANNED_20", "Current + Planned"),
        ("DECLINED_11", "Declined"),
        ("EXPIRED_6", "Expired"),
        ("INCOMPLETE_9", "Incomplete"),
        ("PLANNED_7", "Planned"),
        )

    GRID_REF_DEFAULT_OPTIONS = (
        ("TOPO50_T","TOPO50"),
        ("NZMS260_METRIC_M","NZMS260 (METRIC)"),
        ("LAT_LONG_NZGD2000_D2000","LAT/LONG (NZGD2000)"),
        ("LAT_LONG_NZGD1949_D","LAT/LONG (NZGD1949)"),
        ("NZMG_LONG_REF_L","NZMG (LONG REF)"),
        ("NZTM2000_TM2000","NZTM2000"),
        )

    DATE_TYPE_OPTIONS = (
        ("", "Please Select"),
        ("CANCELLATION_CA","Cancellation"),
        ("CERTIFICATION_CE","Certification"),
        ("COMMENCEMENT_CO","Commencement"),
        ("EXPIRY_EX","Expiry"),
        ("REGISTRATION_RG","Registration"),
        )

    dateOptions={
        'format': 'yyyy-mm-dd',
        'todayHighlight': True,
        'clearBtn': True,
        'autoclose': True,
        'showMeridian' : True
    }
                                               

    licensee_help_text = "Enter the name of the Licensee, or part thereof. Multiple licensees should be separated by commas, e.g. smith, jones. Note: quotes are not required and searches are not case sensitive. Licence Search will find licences with the entered text contained within the licensee's name."
    includeAssociatedLicences_help_text = "If this checkbox is selected, the search will return licences matching the search criteria, including any associated licences."
    location_help_text = "Enter the name of the Location, or part thereof. Multiple locations should be separated by commas, e.g. tower, mast. Note: quotes are not required and searches are not case sensitive. Licence Search will find licences with the entered text contained within the location name."

    licensee = forms.CharField(label="Licensee: ", max_length=200, required=False, help_text=licensee_help_text)
    transmitLocation = forms.CharField(label="Transmit Location: ", max_length=200, required=False, help_text=location_help_text)
    receiveLocation = forms.CharField(label="Receive Location: ", max_length=200, required=False, help_text=location_help_text)
    applicationNumber = forms.IntegerField(label="Application Number: ",required=False)
    callSign = forms.CharField(label="Callsign: ", max_length=10, required=False)
    channel = forms.CharField(label="Channel: ", max_length=200, required=False)
    clientId = forms.IntegerField(label="Client ID: ", required=False)
    dateType = forms.ChoiceField(label="Date Type: ", choices=DATE_TYPE_OPTIONS,required=False)
    fromDate = forms.DateField(label="From Date: ", 
                               required=False, 
                               widget=DateWidget(options=dateOptions))
    fromFrequency = forms.FloatField(label="From Frequency: ", required=False)
    licenceId = forms.IntegerField(label="Licence ID: ", required=False)
    licenceNumber = forms.IntegerField(label="Licence Number: ", required=False)
    licenceStatus = forms.ChoiceField(label="Licence Status: ", choices=LICENCE_STATUS_OPTION,required=False)
    licenceType = forms.ChoiceField(label="Licence Type: ", choices=LICENCE_TYPE_OPTIONS,required=False)
    # locationId = forms.IntegerField(label="Location ID: ", required=False)

    locationId = NoValidationSelect2List(label="Location: ", required=False, widget=autocomplete.ListSelect2(url='get_location'))
    
    managementRightId = forms.IntegerField(label="Management Right ID: ", required=False)
    systemIdentifier = forms.CharField(label="System Identifier: ", max_length=2000,required=False)
    toDate = forms.DateField(label="To Date: ", 
                             required=False,
                             widget=DateWidget(options=dateOptions))
    toFrequency = forms.FloatField(label="To Frequency: ", required=False)
    certifiedBy = forms.ChoiceField(label="Certified By: ", choices=CERTIFIED_BY_OPTIONS,required=False)
    includeAssociatedLicences = forms.BooleanField(label="Include Associated Licences: ", required=False, help_text=includeAssociatedLicences_help_text)
    # gridRefDefault = forms.ChoiceField(label="Grid Reference Default: ", choices=GRID_REF_DEFAULT_OPTIONS,required=False)
    # engineerDecisionIAgree = forms.BooleanField(label="Engineer Decision I Agree: ", required=False)

    def __init__(self, *args, **kwargs):
        super(SearchLicenceForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'class':'has-popover', 'data-content':help_text, 'data-placement':'right', 'data-container':'body'})

class TopupAmountForm(forms.Form):
    '''form that used for topup amount'''
    amount = forms.FloatField(label="Amount", required=True)
