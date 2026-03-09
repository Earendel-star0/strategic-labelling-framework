from gemini_manifold import GeminiManifold

gm = GeminiManifold(initial_mode="Stability")

for i in range(5):
    print(gm.hold([0.2, 0.1]))

print(gm.release())
