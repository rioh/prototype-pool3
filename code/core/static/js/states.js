// us states for typeahead
var usStates = [
    {
        "label": "Alabama",
        "value": "AL"
    },
    {
        "label": "Alaska",
        "value": "AK"
    },
    {
        "label": "Arizona",
        "value": "AZ"
    },
    {
        "label": "Arkansas",
        "value": "AR"
    },
    {
        "label": "California",
        "value": "CA"
    },
    {
        "label": "Colorado",
        "value": "CO"
    },
    {
        "label": "Connecticut",
        "value": "CT"
    },
    {
        "label": "Delaware",
        "value": "DE"
    },
    {
        "label": "District Of Columbia",
        "value": "DC"
    },
    {
        "label": "Florida",
        "value": "FL"
    },
    {
        "label": "Georgia",
        "value": "GA"
    },
    {
        "label": "Hawaii",
        "value": "HI"
    },
    {
        "label": "Idaho",
        "value": "ID"
    },
    {
        "label": "Illinois",
        "value": "IL"
    },
    {
        "label": "Indiana",
        "value": "IN"
    },
    {
        "label": "Iowa",
        "value": "IA"
    },
    {
        "label": "Kansas",
        "value": "KS"
    },
    {
        "label": "Kentucky",
        "value": "KY"
    },
    {
        "label": "Louisiana",
        "value": "LA"
    },
    {
        "label": "Maine",
        "value": "ME"
    },
    {
        "label": "Maryland",
        "value": "MD"
    },
    {
        "label": "Massachusetts",
        "value": "MA"
    },
    {
        "label": "Michigan",
        "value": "MI"
    },
    {
        "label": "Minnesota",
        "value": "MN"
    },
    {
        "label": "Mississippi",
        "value": "MS"
    },
    {
        "label": "Missouri",
        "value": "MO"
    },
    {
        "label": "Montana",
        "value": "MT"
    },
    {
        "label": "Nebraska",
        "value": "NE"
    },
    {
        "label": "Nevada",
        "value": "NV"
    },
    {
        "label": "New Hampshire",
        "value": "NH"
    },
    {
        "label": "New Jersey",
        "value": "NJ"
    },
    {
        "label": "New Mexico",
        "value": "NM"
    },
    {
        "label": "New York",
        "value": "NY"
    },
    {
        "label": "North Carolina",
        "value": "NC"
    },
    {
        "label": "North Dakota",
        "value": "ND"
    },
    {
        "label": "Ohio",
        "value": "OH"
    },
    {
        "label": "Oklahoma",
        "value": "OK"
    },
    {
        "label": "Oregon",
        "value": "OR"
    },
    {
        "label": "Pennsylvania",
        "value": "PA"
    },
    {
        "label": "Rhode Island",
        "value": "RI"
    },
    {
        "label": "South Carolina",
        "value": "SC"
    },
    {
        "label": "South Dakota",
        "value": "SD"
    },
    {
        "label": "Tennessee",
        "value": "TN"
    },
    {
        "label": "Texas",
        "value": "TX"
    },
    {
        "label": "Utah",
        "value": "UT"
    },
    {
        "label": "Vermont",
        "value": "VT"
    },
    {
        "label": "Virginia",
        "value": "VA"
    },
    {
        "label": "Washington",
        "value": "WA"
    },
    {
        "label": "West Virginia",
        "value": "WV"
    },
    {
        "label": "Wisconsin",
        "value": "WI"
    },
    {
        "label": "Wyoming",
        "value": "WY"
    }
];

// state counts for state chart
var stateCounts = [
    {
        "code": "FL",
        "value": 0
    },
    {
        "code": "IL",
        "value": 0
    },
    {
        "code": "TN",
        "value": 0
    },
    {
        "code": "WA",
        "value": 0
    },
    {
        "code": "NJ",
        "value": 0
    },
    {
        "code": "MI",
        "value": 0
    },
    {
        "code": "PA",
        "value": 0
    },
    {
        "code": "NC",
        "value": 0
    },
    {
        "code": "CA",
        "value": 0
    },
    {
        "code": "NY",
        "value": 0
    },
    {
        "code": "OR",
        "value": 0
    },
    {
        "code": "TX",
        "value": 0
    },
    {
        "code": "NV",
        "value": 0
    },
    {
        "code": "GA",
        "value": 0
    },
    {
        "code": "MA",
        "value": 0
    },
    {
        "code": "OH",
        "value": 0
    },
    {
        "code": "IA",
        "value": 0
    },
    {
        "code": "NE",
        "value": 0
    },
    {
        "code": "IN",
        "value": 0
    },
    {
        "code": "OK",
        "value": 0
    },
    {
        "code": "AL",
        "value": 0
    },
    {
        "code": "MO",
        "value": 0
    },
    {
        "code": "WV",
        "value": 0
    },
    {
        "code": "KS",
        "value": 0
    },
    {
        "code": "AZ",
        "value": 0
    },
    {
        "code": "CO",
        "value": 0
    },
    {
        "code": "SC",
        "value": 0
    },
    {
        "code": "MN",
        "value": 0
    },
    {
        "code": "MD",
        "value": 0
    },
    {
        "code": "ID",
        "value": 0
    },
    {
        "code": "KY",
        "value": 0
    },
    {
        "code": "WI",
        "value": 0
    },
    {
        "code": "VA",
        "value": 0
    },
    {
        "code": "CT",
        "value": 0
    },
    {
        "code": "UT",
        "value": 0
    },
    {
        "code": "AR",
        "value": 0
    },
    {
        "code": "NH",
        "value": 0
    },
    {
        "code": "MS",
        "value": 0
    },
    {
        "code": "DE",
        "value": 0
    },
    {
        "code": "WY",
        "value": 0
    },
    {
        "code": "SD",
        "value": 0
    },
    {
        "code": "NM",
        "value": 0
    },
    {
        "code": "LA",
        "value": 0
    },
    {
        "code": "VT",
        "value": 0
    },
    {
        "code": "ME",
        "value": 0
    },
    {
        "code": "MT",
        "value": 0
    },
    {
        "code": "ND",
        "value": 0
    },
    {
        "code": "RI",
        "value": 0
    },
    {
        "code": "HI",
        "value": 0
    },
    {
        "code": "AK",
        "value": 0
    }
];
