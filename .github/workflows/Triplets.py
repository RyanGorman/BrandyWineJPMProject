def find_pairs(nums, m):
    pairs = []
    n = len(nums)
    for j in range(n):
        for k in range(j + 1, n):
            if nums[j] + nums[k] == m:
                pairs.append((nums[j], nums[k]))
    return pairs

def find_triplets(nums):
    triplets = set()
    n = len(nums)
    for i in range(n):
        m = -nums[i]
        pairs = find_pairs(nums[i+1:], m)
        for pair in pairs:
            triplet = tuple(sorted((nums[i], pair[0], pair[1])))
            triplets.add(triplet)
    return list(triplets)

nums = [-5, 4, -4, 3, -3, -2, 2, -1, 1, 0]
triplets = find_triplets(nums)
print("Unique triplets that sum to 0 are:", triplets)
