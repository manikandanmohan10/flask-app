from src.blueprint.bp import AuthBlueprint, QuoteBlueprint, \
    ToDoBluprint, WTFFormBlueprint

blueprints = []
blueprints.append(AuthBlueprint())
blueprints.append(QuoteBlueprint())
blueprints.append(ToDoBluprint())
blueprints.append(WTFFormBlueprint())