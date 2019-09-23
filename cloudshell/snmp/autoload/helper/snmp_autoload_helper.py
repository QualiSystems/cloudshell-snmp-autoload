def log_autoload_details(logger, autoload_details):
    """Logging autoload details.

    :param autoload_details:
    :return:
    """
    logger.debug("-------------------- <RESOURCES> ----------------------")
    for resource in autoload_details.resources:
        logger.debug(
            "{0:15}, {1:20}, {2}".format(
                str(resource.relative_address),
                resource.name,
                resource.unique_identifier,
            )
        )
    logger.debug("-------------------- </RESOURCES> ----------------------")

    logger.debug("-------------------- <ATTRIBUTES> ---------------------")
    for attribute in autoload_details.attributes:
        logger.debug(
            "-- {0:15}, {1:60}, {2}".format(
                str(attribute.relative_address),
                attribute.attribute_name,
                attribute.attribute_value,
            )
        )
    logger.debug("-------------------- </ATTRIBUTES> ---------------------")
