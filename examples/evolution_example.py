from gemini_manifold import GeminiManifold

gm = GeminiManifold(initial_mode="Evolution")

print(gm.status())
gm.resolve_mode("Expressive", human_weight=0.7)
print(gm.status())
