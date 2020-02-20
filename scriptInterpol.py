import urllib.request
import pymisp
import json

from datetime import date
from pymisp import ExpandedPyMISP, MISPEvent

def submit_to_misp(misp, misp_event, misp_objects):
    '''
    Submit a list of MISP objects to a MISP event
    :misp: PyMISP API object for interfacing with MISP
    :misp_event: MISPEvent object
    :misp_objects: List of MISPObject objects. Must be a list
    '''
# go through round one and only add MISP objects
    for misp_object in misp_objects:
        template_id = misp.get_object_template_id(misp_object.template_uuid)
        misp.add_object(misp_event.id, template_id, misp_object)
    # go through round two and add all the object references for each object
    for misp_object in misp_objects:
        for reference in misp_object.ObjectReference:
            misp.add_object_reference(reference)

#Event settings
event = MISPEvent()
event.info = 'New event'
event.distribution = 0
event.threat_level_id = 2
event.analysis = 1
event.set_date(date.today())

#

misp_url = "https://192.168.40.129:8443"
misp_key = "QWJveTdNk8eLowBZM9VG2JR0jGOFY6oLKAsyFs1D"
misp_verifycert = False
#
misp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert)
# response = api.add_object
# if response['error']:
#     print("error")
# else:
#     print("ok")

# last_name = misp_object.add_attribute('present-family-name')
# forname = misp_object.add_attribute('forname')
# gender = misp_object.add_attribute('sex')
# date_of_birth = misp_object.add_attribute('date-of-birth')
# place_of_birth = misp_object.add_attribute('place-of-birth')
# nationality = misp_object.add_attribute('nationality')
# height = misp_object.add_attribute('height')
# weight = misp_object.add_attribute('weight')
# hair_colour = misp_object.add_attribute('colour-of-hair')
# eye_colour = misp_object.add_attribute('colour-of-eyes')
# spoken_languages = misp_object.add_attribute('language-spoken')
# violation = misp_object.add_attribute('violation')
# distinguishing_marks_and_characteristics = misp_object.add_attribute('distinguishing-marks-and-characteristics')
# date_of_disparition = misp_object.add_attribute('date-of-disparition')
# place_of_disparition = misp_object.add_attribute('place-of-disparition')


#result by page


URL="https://ws-public.interpol.int/notices/v1/red?resultPerPage=20000&page=1"
with urllib.request.urlopen(URL) as url:
    data = json.loads(url.read().decode())
    objects = []
    for i in range(len(data["_embedded"]["notices"])):
        misp_object = pymisp.MISPObject('interpol-notice')
        misp_object.add_attribute('present-family-name', data["_embedded"]["notices"][i]["name"])
        misp_object.add_attribute('forename', data["_embedded"]["notices"][i]["forename"])
        #misp_object.add_attribute('entity_id', data["_embedded"]["notices"][i]["entity_id"])
        misp_object.add_attribute('date-of-birth', data["_embedded"]["notices"][i]["date_of_birth"])
        misp_object.add_attribute('nationality', data["_embedded"]["notices"][i]["nationalities"])

        objects.append(misp_object)


    submit_to_misp(misp, event, objects)

        # misp_object.add_attribute('place-of-birth')
        # misp_object.add_attribute('height')
        # misp_object.add_attribute('weight')
        # misp_object.add_attribute('colour-of-hair')
        # misp_object.add_attribute('colour-of-eyes')
        # misp_object.add_attribute('language-spoken')
        # misp_object.add_attribute('violation')
        # misp_object.add_attribute('distinguishing-marks-and-characteristics')
        # misp_object.add_attribute('date-of-disparition')
        # misp_object.add_attribute('place-of-disparition')
