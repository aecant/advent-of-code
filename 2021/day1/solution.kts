import kotlin.io.path.Path
import kotlin.io.path.readLines

fun parseDepths(filename: String) =
    Path(filename).readLines().map { it.toInt() }

fun countIncreasedPart1(depths: List<Int>) =
    depths.windowed(2).count { (a, b) -> b > a }

fun countIncreasedPart2(depths: List<Int>) =
    depths.windowed(3).windowed(2).count { (w1, w2) -> w2.sum() > w1.sum() }

val depths = parseDepths("input.txt")

check(countIncreasedPart1(depths) == 1298)
check(countIncreasedPart2(depths) == 1248)
