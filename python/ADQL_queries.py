import time

import pyvo as vo

def use_case_queries(url, use_case_nos):
    '''
    Function to evaluate use case queries on a result
    :param url: url of metadata database
    :param use_case_nos: list of use case numbers to evaluate
    :returns: timing and length of use case queries
    '''
    service = vo.dal.TAPService(url)

    # change to be specific to an upload name when there is more than one observation uploaded
    resultset = service.search("SELECT * FROM derivedobservation")
    derived_observation_id = resultset.to_table()['id'][0]

    resultset = service.search("""
    SELECT t.name, p.* FROM Target t 
    JOIN Observation o ON o.target_id = t.id 
    JOIN point p ON t.id = p.id
    WHERE EXISTS (
        SELECT 1
        FROM Derivedobservation d 
        WHERE d.id = '{}' AND d.members LIKE '%' || o.uri || '%'
        )

    ;""".format(derived_observation_id))

    x = resultset['cval1'][0]
    y = resultset['cval2'][0]

    query_dictionary = {
        "1": ["""
        SELECT t.*, i.* FROM Telescope t 
        JOIN Observation o ON o.telescope_id = t.id 
        JOIN Instrument i ON i.id = o.instrument_id
        WHERE EXISTS (
            SELECT 1
            FROM Derivedobservation d 
            WHERE d.id = '{}' AND d.members LIKE '%' || o.uri || '%'
            )
        ;""".format(derived_observation_id),

        """
        SELECT t.name, p.* FROM Target t 
        JOIN Observation o ON o.target_id = t.id 
        JOIN point p ON t.id = p.id
        WHERE EXISTS (
            SELECT 1
            FROM Derivedobservation d 
            WHERE d.id = '{}' AND d.members LIKE '%' || o.uri || '%'
            )
        
        ;""".format(derived_observation_id),

              """
              SELECT pl.*, t.bounds_upper, t.bounds_lower, e.bounds_upper, e.bounds_lower, p.states, pvn.project FROM Plane pl 
              JOIN Observation o ON o.id = pl.observation_id 
              JOIN time t ON pl.time_id = t.id
              JOIN energy e ON pl.energy_id = e.id
              JOIN polarization p ON pl.polarization_id = p.id
              JOIN provenance pvn ON pl.provenance_id = pvn.id
              WHERE EXISTS (
                  SELECT 1
                  FROM Derivedobservation d 
                  WHERE d.id = '{}' AND d.members LIKE '%' || o.uri || '%'
                  )
              ;""".format(derived_observation_id)
        ],

        "3": ["""
        SELECT p.* FROM provenance p
        JOIN Plane pl ON pl.provenance_id = p.id 
        JOIN Observation o ON o.id = pl.observation_id
        WHERE EXISTS (
            SELECT 1
            FROM Derivedobservation d 
            WHERE d.id = '{}' AND d.members LIKE '%' || o.uri || '%'
            )
        """.format(derived_observation_id)],

        "4": ["""
        SELECT p.project, p.producer, o.uri FROM provenance p
        JOIN Plane pl ON pl.provenance_id = p.id 
        JOIN Observation o ON o.id = pl.observation_id
        WHERE EXISTS (
            SELECT 1
            FROM Derivedobservation d 
            WHERE d.id = '{}' AND d.members LIKE '%' || o.uri || '%'
            )
        """.format(derived_observation_id)],


        "5": ["""
        SELECT o.uri, p.cval1, p.cval2 
        FROM point p
        JOIN targetposition tp ON tp.id = p.id
        JOIN observation o ON tp.id = o.targetposition_id
        WHERE p.cval1 > {0} AND p.cval1 < {1} AND p.cval2 > {2} AND p.cval2 < {3}
        """.format(str(x-0.5), str(x+0.5), str(y-0.5), str(y+0.5))],

        "6": ["""
        SELECT p.observation_id, p.uri, pr.keywords FROM Plane p
        JOIN Provenance pr ON p.provenance_id = pr.id
        """],

        "7": ["""
        SELECT o.uri, pr.name, pr.version, p.datarelease, a.uri, a.contenttype, a.contentrelease FROM Observation o 
        JOIN Plane p ON o.id=p.observation_id
        JOIN Provenance pr ON pr.id = p.provenance_id
        JOIN Artifact a ON a.plane_id = p.id
        """],

        "8": ["""
        SELECT pr.lastexecuted, a.contentlength, a.uri FROM Plane p
        JOIN Provenance pr ON pr.id = p.provenance_id
        JOIN Artifact a ON a.plane_id = p.id
        """],

        "9": ["""
        SELECT pr.lastexecuted, a.contentlength, a.uri FROM Plane p
        JOIN Provenance pr ON pr.id = p.provenance_id
        JOIN Artifact a ON a.plane_id = p.id
        """],

        "10": ["""
        SELECT pl.*, t.bounds_upper, t.bounds_lower, e.bounds_upper, e.bounds_lower, p.states, pvn.project FROM Plane pl 
        JOIN Observation o ON o.id = pl.observation_id 
        JOIN time t ON pl.time_id = t.id
        JOIN energy e ON pl.energy_id = e.id
        JOIN polarization p ON pl.polarization_id = p.id
        JOIN provenance pvn ON pl.provenance_id = pvn.id
        WHERE EXISTS (
            SELECT 1
            FROM Derivedobservation d 
            WHERE d.id = '{}' AND d.members LIKE '%' || o.uri || '%'
            )
        ;""".format(derived_observation_id)],

        "11": ["""
        SELECT pr.lastexecuted, a.uri, pr.project, p.datarelease, p.metarelease, o.metarelease FROM Plane p
        JOIN Provenance pr ON pr.id = p.provenance_id
        JOIN Artifact a ON a.plane_id = p.id
        JOIN Observation o ON o.id = p.observation_id
        """],

        "12": ["""
        SELECT o.id, t.bounds_lower, t.bounds_upper, pr.name, pr.version FROM Observation o 
        JOIN Plane p ON o.id = p.observation_id
        JOIN time t ON t.id = p.time_id
        JOIN Provenance pr ON pr.id = provenance_id
        """,
        """
        SELECT o.id, o.uri, t.geolocationx, t.geolocationy, t.geolocationz, i.name FROM Observation o
        JOIN Telescope t ON t.id = o.telescope_id
        JOIN Instrument i ON i.id = o.instrument_id
        WHERE EXISTS (
            SELECT 1
            FROM Derivedobservation d 
            WHERE d.id = '{}' AND d.members LIKE '%' || o.uri || '%'
            )
        """.format(derived_observation_id)],

        "13": ["""
        SELECT o.uri, pr.name, pr.version, p.datarelease, a.uri, a.contenttype, a.contentrelease, pr.project
        FROM Observation o 
        JOIN Plane p ON o.id=p.observation_id
        JOIN Provenance pr ON pr.id = p.provenance_id
        JOIN Artifact a ON a.plane_id = p.id
        """],

        "14": ["""
        SELECT o.uri, pr.name, pr.version, p.datarelease, a.uri, a.contenttype, a.contentrelease FROM Observation o 
        JOIN Plane p ON o.id=p.observation_id
        JOIN Provenance pr ON pr.id = p.provenance_id
        JOIN Artifact a ON a.plane_id = p.id
        """],

        "15": ["""
        SELECT pr.lastexecuted, a.uri, pr.project, p.datarelease, p.metarelease, o.metarelease, o.intent FROM Plane p
        JOIN Provenance pr ON pr.id = p.provenance_id
        JOIN Artifact a ON a.plane_id = p.id
        JOIN Observation o ON o.id = p.observation_id
        """],

        "16": ["""
        SELECT pr.lastexecuted, a.uri, pr.project, p.datarelease FROM Plane p
        JOIN Provenance pr ON pr.id = p.provenance_id
        JOIN Artifact a ON a.plane_id = p.id
        JOIN Observation o ON o.id = p.observation_id
        """]

    }

    timings = {}
    results = {}

    for q_no in use_case_nos:
        print('query number :', q_no)
        query = query_dictionary[str(q_no)]
        t0 = time.time()
        results_length = 0
        # print(query)
        for sub_query in query:
            query_result = service.search(sub_query)
            results_length += len(query_result)
        timings[str(q_no)] = time.time() - t0
        results[str(q_no)] = results_length

    return timings, results



