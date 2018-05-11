import logging

logger = logging.getLogger('wise.content.migration')
default_profile = 'profile-wise.content:default'


def upgrade_to_2(context):
    logger.info("Upgrading to 2")

    # need to reimport wise.content, it has updated workflow settings
    context.runImportStepFromProfile(default_profile, 'workflow')


def upgrade_to_3(context):
    logger.info("Upgrading to 3")

    # need to reimport wise.content, it has updated workflow settings
    context.runImportStepFromProfile(default_profile, 'workflow')


def upgrade_to_4(context):
    logger.info("Upgrading to 4")

    # need to reimport wise.content, it has updated type settings
    context.runImportStepFromProfile(default_profile, 'typeinfo')

    logger.info("Upgrade finished.")


def upgrade_to_5(context):
    logger.info("Upgrading to 5")

    # need to reimport wise.content, it has updated type settings
    context.runImportStepFromProfile(default_profile, 'typeinfo')
    context.runImportStepFromProfile(default_profile, 'repositorytool')
    context.runImportStepFromProfile(default_profile, 'contentrules')

    logger.info("Upgrade finished.")


def upgrade_to_6(context):
    logger.info("Upgrading to 6")

    # need to reimport wise.content, it has updated actions settings
    context.runImportStepFromProfile(default_profile, 'actions')

    logger.info("Upgrade finished.")


def upgrade_to_7(context):
    logger.info("Upgrading to 7")

    # need to reimport wise.content, it has updated control panel settings
    context.runImportStepFromProfile(default_profile, 'controlpanel')
    context.runImportStepFromProfile(default_profile, 'propertiestool')

    logger.info("Upgrade finished.")
