from src.blueprint.bp import AuthBlueprint, QuoteBlueprint, ToDoBluprint

blueprints = []
blueprints.append(AuthBlueprint())
blueprints.append(QuoteBlueprint())
blueprints.append(ToDoBluprint())