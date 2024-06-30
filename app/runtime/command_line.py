import os
import argparse
from app.models import CommandLineArgs
from app.models.currencies import Currencies
from app.models.impact_class import ImpactClass
from app.models.time_period import TimePeriod


class CommandLine:
    @staticmethod
    def parse_arguments() -> CommandLineArgs:
        parser = argparse.ArgumentParser(
            description='Run the application with specified impact classes, currencies, time period, and output folder.')

        parser.add_argument(
            '--impact-classes',
            type=str,
            help='Comma-separated list of impact classes (yellow, orange, red, gray)',
            default=''
        )

        parser.add_argument(
            '--currencies',
            type=str,
            help='Comma-separated list of currencies (AUD, CAD, CHF, EUR, GBP, JPY, NZD, USD)',
            default=''
        )

        parser.add_argument(
            '--time-period',
            type=str,
            help='Time period (Tomorrow, Next Week, Next Month, Today, This Week, This Month, Yesterday, Last Week, Last Month)',
            default=''
        )

        parser.add_argument(
            '--output-folder',
            type=str,
            help='Folder where the output files will be saved',
            default=os.getcwd()
        )

        parser.add_argument(
            '--nnfx',
            action='store_true',
            help='Boolean switch that is true if specified and false if not'
        )

        parser.add_argument(
            '--custom-nnfx-filters',
            type=str,
            help='Path to a custom NNFX filters JSON file'
        )

        parser.add_argument(
            '--custom-calendar-template',
            type=str,
            help='Path to a custom calendar template file'
        )

        args = parser.parse_args()

        # Process impact classes
        if args.impact_classes:
            impact_classes = [ImpactClass.from_text(
                ic.strip()) for ic in args.impact_classes.split(',')]
        else:
            impact_classes = []

        # Process currencies
        if args.currencies:
            currencies = [Currencies.from_text(
                curr.strip()) for curr in args.currencies.split(',')]
        else:
            currencies = []

        # Process time period
        time_period = None
        if args.time_period:
            time_period = TimePeriod.from_text(args.time_period.strip())

        # Process output folder
        output_folder = args.output_folder

        # Process nnfx flag
        nnfx = args.nnfx

        # Process custom NNFX filters file
        custom_nnfx_filters = args.custom_nnfx_filters

        # Process custom calendar template file
        custom_calendar_template = args.custom_calendar_template

        return CommandLineArgs(
            impact_classes=impact_classes,
            currencies=currencies,
            time_period=time_period,
            output_folder=output_folder,
            nnfx=nnfx,
            custom_nnfx_filters=custom_nnfx_filters,
            custom_calendar_template=custom_calendar_template
        )