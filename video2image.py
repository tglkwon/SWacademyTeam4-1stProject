import imageio.v3 as iio

path = "videos/All New Popeye - The Ski's The Limit AND MORE (Episode 2).mp4"
# read a single frame
frame = iio.imread(
    path,
    index=42,
    plugin="pyav",
)

# bulk read all frames
# Warning: large videos will consume a lot of memory (RAM)
frames = iio.imread(path, plugin="pyav")

# iterate over large videos
for frame in iio.imiter(path, plugin="pyav"):
    print(frame.shape, frame.dtype)
