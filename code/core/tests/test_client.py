import json
from mock import patch
from django.test import TestCase

from core.api_client import ApiResult

class ApiResultTestCase(TestCase):
    def setUp(self):
        pass 

    def test_lookup(self):
        test_dictionary = json.loads('{"openfda": "testing"}')
        test_string = 'openfda'
        result = ApiResult({})
        value = result.lookup(test_dictionary, test_string)
        self.assertEquals(value, 'testing')

        test_dictionary = json.loads('{"openfda": {"brand_name": "testing"}}')
        test_string = 'openfda.brand_name'
        value = result.lookup(test_dictionary, test_string)
        self.assertEquals(value, 'testing')

    def test_lookup_default(self):
        test_dictionary = json.loads('{"openfda": {"brand_name": "testing"}}')
        test_string = 'openfda.brand'
        result = ApiResult({})
        value = result.lookup(test_dictionary, test_string, "xyz")
        self.assertEquals(value, 'xyz')
        
    def test_clean_labels(self):
        test_dictionary = json.loads("""
          {"meta": {
            "results": {
              "skip": 0,
              "limit": 1,
              "total": 72590
            }
          },
          "results": [
            {
              "dosage_and_administration": [
                "Directions Protection"
              ],
              "id": "f229e866-5775-4e42-a316-8480dd92fec6",
              "active_ingredient": [
                "BRONZE ACTIVE INGREDIENTS: TITANIUM DIOXIDE 2 %"
              ],
              "inactive_ingredient": [
                "INGREDIENTS: TALC, POLYMETHYL METHACRYLATE"
              ],
              "openfda": {
                "spl_id": [
                  "50de8449-69cf-4593-bdac-4aae7e7b4b7b"
                ],
                "route": [
                  "TOPICAL"
                ],
                "substance_name": [
                  "OCTINOXATE",
                  "TITANIUM DIOXIDE",
                  "ZINC OXIDE"
                ],
                "generic_name": [
                  "TITANIUM DIOXIDE, OCTINOXATE, ZINC OXIDE"
                ],
                "manufacturer_name": [
                  "Chantecaille Beaute Inc"
                ],
                "brand_name": [
                  "CHANTECAILLE"
                ]
              }
            }]}
        """)
        result = ApiResult(test_dictionary)
        meta, results = result.clean_labels()
        self.assertEquals(meta['total'], 72590)

    def test_clean_events(self):
        test_dictionary = json.loads("""
        {
          "meta": {
            "results": {
              "skip": 0,
              "limit": 1,
              "total": 4587031
            }
          },
          "results": [
            {
              "safetyreportid": "4322505-4",
              "receiver": null,
              "receivedateformat": "102",
              "receiptdateformat": "102",
              "primarysource": null,
              "receivedate": "20040319",
              "seriousnessother": "1",
              "patient": {
                "patientonsetage": "56",
                "patientonsetageunit": "801",
                "drug": [
                  {
                    "drugtreatmentdurationunit": "804",
                    "drugauthorizationnumb": "50621",
                    "drugtreatmentduration": "4",
                    "drugstartdateformat": "102",
                    "drugcharacterization": "1",
                    "drugindication": "PYELONEPHRITIS",
                    "medicinalproduct": "OROKEN (CEFIXIME, UNSPEC)",
                    "drugadministrationroute": "048",
                    "drugdosagetext": "ORAL",
                    "drugstartdate": "20031227",
                    "drugenddate": "20031230",
                    "drugenddateformat": "102"
                  },
                  {
                    "drugcharacterization": "2",
                    "medicinalproduct": "ROCEPHIN",
                    "openfda": {
                      "unii": [
                        "75J73V1629"
                      ],
                      "spl_id": [
                        "86e3103c-9d8b-4693-b5db-3fd62330c754"
                      ],
                      "substance_name": [
                        "CEFTRIAXONE SODIUM"
                      ],
                      "product_type": [
                        "HUMAN PRESCRIPTION DRUG"
                      ],
                      "pharm_class_cs": [
                        "Cephalosporins [Chemical/Ingredient]"
                      ],
                      "manufacturer_name": [
                        "Genentech, Inc."
                      ],
                      "brand_name": [
                        "ROCEPHIN"
                      ],
                      "route": [
                        "INTRAMUSCULAR",
                        "INTRAVENOUS"
                      ],
                      "pharm_class_epc": [
                        "Cephalosporin Antibacterial [EPC]"
                      ],
                      "generic_name": [
                        "CEFTRIAXONE SODIUM"
                      ]
                    }
                  },
                  {
                    "drugcharacterization": "2",
                    "medicinalproduct": "OFLOXACIN",
                    "openfda": {
                      "unii": [
                        "A4P49JAZ9H"
                      ],
                      "substance_name": [
                        "OFLOXACIN"
                      ],
                      "product_type": [
                        "HUMAN PRESCRIPTION DRUG"
                      ],
                      "pharm_class_cs": [
                        "Quinolones [Chemical/Ingredient]"
                      ],
                      "manufacturer_name": [
                        "Akorn, Inc.",
                        "Altaire Pharmaceuticals Inc.",
                        "Dr. Reddy's Laboratories Limited",
                        "Pack Pharmaceuticals, LLC",
                        "Hi-Tech Pharmacal Co., Inc.",
                        "Allergan, Inc.",
                        "Bausch & Lomb Incorporated",
                        "Apotex Corp.",
                        "Cadila Pharmaceuticals Limited",
                        "PharmaForce, Inc.",
                        "Falcon Pharmaceuticals, Ltd.",
                        "Teva Pharmaceuticals USA Inc"
                      ],
                      "brand_name": [
                        "OFLOXACIN OTIC",
                        "OFLOXACIN OPHTHALMIC",
                        "OFLOXACIN",
                        "OCUFLOX"
                      ],
                      "route": [
                        "AURICULAR (OTIC)",
                        "ORAL",
                        "OPHTHALMIC"
                      ],
                      "nui": [
                        "N0000175937",
                        "N0000007606"
                      ],
                      "pharm_class_epc": [
                        "Quinolone Antimicrobial [EPC]"
                      ],
                      "generic_name": [
                        "OFLOXACIN",
                        "OFLOXAXIN"
                      ]
                    }
                  }
                ],
                "patientsex": "1"
              },
              "receiptdate": "20040315",
              "transmissiondate": "20041129",
              "transmissiondateformat": "102",
              "seriousnesshospitalization": "1",
              "serious": "1",
              "companynumb": "HQWYE821915MAR04"
            }
          ]
        }
        """)
        result = ApiResult(test_dictionary)
        meta, results = result.clean_labels()
        self.assertEquals(meta['total'], 4587031)

    def test_clean_enforcements(self):
        test_dictionary = json.loads("""
        {
          "meta": {
            "results": {
              "skip": 0,
              "limit": 1,
              "total": 3769
            }
          },
          "results": [
            {
              "recall_number": "D-0167-2015",
              "reason_for_recall": "Lack of Assurance of Sterility:...",
              "status": "Ongoing",
              "distribution_pattern": "Nationwide",
              "product_quantity": "60 mL",
              "recall_initiation_date": "20140827",
              "state": "IL",
              "event_id": "69152",
              "product_type": "Drugs",
              "product_description": "Tri-mix T50, 8.825 mg/0.29 mg/2.95 mcg/mL...",
              "country": "US",
              "city": "Naperville",
              "recalling_firm": "Martin Avenue Pharmacy, Inc.",
              "report_date": "20141105",
              "@epoch": 1424553174.836488,
              "voluntary_mandated": "Voluntary: Firm Initiated",
              "classification": "Class II",
              "code_info": "Lot Number: 07142014@48, Exp 9/30/2014",
              "@id": "000d4ccfcaf0512bd20916cdd38775d2757118fcbafcdd7ea735f16d88622103",
              "openfda": {
                "manufacturer_name": [
                  "Pharmacia and Upjohn Company"
                ]},
              "initial_firm_notification": "Two or more of the following: Email, Fax, Letter, Press Release, Telephone, Visit"
            }
          ]
        }
        """)
        result = ApiResult(test_dictionary)
        meta, results = result.clean_labels()
        self.assertEquals(meta['total'], 3769)
