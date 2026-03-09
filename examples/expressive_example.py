from gemini_manifold import GeminiManifold

gm = GeminiManifold(initial_mode="Expressive")

print(gm.hold([1, 0]))
print(gm.hold([0, 1]))
print(gm.release())
