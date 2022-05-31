#!/usr/bin/env python3
"""Software for managing and analysing patients' inflammation data in our imaginary hospital."""

import argparse

from inflammation import models, views, serializers


def main(args):
    """The MVC Controller of the patient inflammation data system.

    The Controller is responsible for:
    - selecting the necessary models and views for the current task
    - passing data between models and views
    """
    in_files = args.infiles
    if not isinstance(in_files, list):
        in_files = [args.infiles]

    for filename in in_files:
        inflammation_data = models.load_csv(filename)

        if args.view == "visualize":
            view_data = {
                "average": models.daily_mean(inflammation_data),
                "max": models.daily_max(inflammation_data),
                "min": models.daily_min(inflammation_data),
            }

            views.visualize(view_data)

        elif args.view == "record":
            patient_data = inflammation_data[args.patient]
            observations = [
                models.Observation(day, value) for day, value in enumerate(patient_data)
            ]
            patient = models.Patient("UNKNOWN", observations)
            views.display_patient_record(patient)

            if args.save:
                patient_data = inflammation_data[args.patient]
                observations = [
                    models.Observation(day, value)
                    for day, value in enumerate(patient_data)
                ]
                patient = models.Patient("UNKNOWN", observations)
                serializers.PatientJSONSerializer.save([patient], args.filename)
                print(
                    "patient %s  data saved to file %s" % (args.patient, args.filename)
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A basic patient inflammation data management system"
    )
    parser.add_argument(
        "infiles",
        nargs="+",
        help="Input CSV(s) containing inflammation series for each patient",
    )
    parser.add_argument(
        "--view",
        default="visualize",
        choices=["visualize", "record"],
        help='Switch for visualisation option. "Visualize" plots results graphically, "record" prints the data for '
        "a single patient, as specified by the --patient option",
    )

    parser.add_argument(
        "--patient",
        type=int,
        default=0,
        help="Integer index of the patient record to visualise (used in conjuction with --visualize). Default is 0.",
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Filename to save the patient data specified from --visualize"
        " and --patient options. Data is output in JSON format",
    )

    args = parser.parse_args()
    main(args)
