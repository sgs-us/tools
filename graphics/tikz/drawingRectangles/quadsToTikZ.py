import numpy as np
from math import cos, sin, pi
'''
note: to use this file within tikz you have to add the following definition to your tex file:
\makeatletter
\tikzoption{canvas is xy plane at z}[]{%
  \def\tikz@plane@origin{\pgfpointxyz{0}{0}{#1}}%
  \def\tikz@plane@x{\pgfpointxyz{1}{0}{#1}}%
  \def\tikz@plane@y{\pgfpointxyz{0}{1}{#1}}%
  \tikz@canvas@is@plane
}
\makeatother

\tikzset{xyp/.style={canvas is xy plane at z=#1}}
\tikzset{xzp/.style={canvas is xz plane at y=#1}}
\tikzset{yzp/.style={canvas is yz plane at x=#1}}
'''


def quad2D(lowerLeft, upperRight, TeXargs=''):
    if TeXargs == '':
        print(r"\draw (%f, %f) rectangle (%f, %f);" % (lowerLeft[0], lowerLeft[1],
                                                       upperRight[0], upperRight[1]))
    else:
        print(r"\draw[%s] (%f, %f) rectangle (%f, %f);" %
              (TeXargs, lowerLeft[0], lowerLeft[1],
               upperRight[0], upperRight[1]))


def quad3D(backLowerLeft, frontUpperRight, TeXargs=''):
    print(r"\draw[xyp=%f,%s] (%f, %f) rectangle (%f, %f);" %
          (backLowerLeft[2], TeXargs,
           backLowerLeft[0], backLowerLeft[1],
           frontUpperRight[0], frontUpperRight[1]))
    print(r"\draw[xyp=%f,%s] (%f, %f) rectangle (%f, %f);" %
          (frontUpperRight[2], TeXargs,
           backLowerLeft[0], backLowerLeft[1],
           frontUpperRight[0], frontUpperRight[1]))

    print(r"\draw[xzp=%f,%s] (0, 0) (%f, %f) rectangle (%f, %f);" %
          (backLowerLeft[1], TeXargs,
           backLowerLeft[0], backLowerLeft[2],
           frontUpperRight[0], frontUpperRight[2]))
    print(r"\draw[xzp=%f,%s] (%f, %f) rectangle (%f, %f);" %
          (frontUpperRight[1], TeXargs,
           backLowerLeft[0], backLowerLeft[2],
           frontUpperRight[0], frontUpperRight[2]))

    print(r"\draw[yzp=%f,%s] (%f, %f) rectangle (%f, %f);" %
          (backLowerLeft[0], TeXargs,
           backLowerLeft[1], backLowerLeft[2],
           backLowerLeft[1], frontUpperRight[2]))
    print(r"\draw[yzp=%f,%s] (%f, %f) rectangle (%f, %f);" %
          (frontUpperRight[0], TeXargs,
           backLowerLeft[1], backLowerLeft[2],
           frontUpperRight[1], frontUpperRight[2]))
    print("\n")


def drawCurve2D(pts):
    print(r" \draw [color=red]")
    for p in pts:
        if p != pts[-1]:
            print(r"(%f, %f) -- " % (p[0], p[1]))
        else:
            print(r"(%f, %f);" % (p[0], p[1]))


def gridFromEnc2D(enc, drawTree=False, showCurve=False, showVirtualLayer=False):
    level = 0
    lctr = [0]
    curvePts = []
    quads = []
    if drawTree:
        treeCode = r"\graph [tree layout, grow=down, fresh nodes, level distance=1.25cm, sibling distance=1cm]"
        treeCode += "\n{\n"

    # function to increment the level counter; includes completion of blocks
    def incrLCtr(l, drawTree):
        nonlocal level
        nonlocal treeCode
        if lctr[l] < 3:
            lctr[l] += 1
        else:
            lctr[l] = 0
            incrLCtr(l - 1, drawTree)
            level -= 1
            if drawTree:
                treeCode += "},\n" if level >= 1 else "}\n"

    # process encoding and draw child cells (i.e. all unrefined cells)
    if enc == '0':
        quad2D([0, 0], [1, 1])
    else:
        for c in enc:
            if c == '1':
                level += 1
                if len(lctr) < level + 1:
                    lctr.append(0)
                if drawTree:
                    treeCode += "\"$\\circ$\" -> {\n"
            else:
                pos = [[0, 0], [1, 1]]
                if showCurve:
                    crv = [0, 0]
                if len(lctr) < level:
                    lctr.append(0)
                for i in range(level + 1):
                    if lctr[i] % 2 == 1:
                        pos[0][0] += 1. / float(1 << i)
                    if lctr[i] > 1:
                        pos[0][1] += 1. / float(1 << i)
                pos[1][0] = pos[0][0] + 1. / float(1 << level)
                pos[1][1] = pos[0][1] + 1. / float(1 << level)
                quads.append(pos)
                if showCurve:
                    crv[0] = pos[0][0] + 1. / float(1 << (level + 1))
                    crv[1] = pos[0][1] + 1. / float(1 << (level + 1))
                    curvePts.append(crv)
                if drawTree:
                    treeCode += "\"$\\circ$\",\n" if lctr[level] < 3 else "\"$\\circ$\"\n"
                incrLCtr(level, drawTree)
        if drawTree:
            treeCode += "\n};\n"

    for q in quads:
        quad2D(q[0], q[1])
    if showCurve:
        drawCurve2D(curvePts)
    if drawTree:
        print(r"\begin{scope}")
        print(
            r"\pgftransformcm{%f}{0}{0}{%f}{\pgfpoint{3 cm}{1 cm}}" %
            (1. / len(lctr), 1. / len(lctr)))
        print(treeCode)
        print(r"\end{scope}")


def drawCurve3D(pts):
    print(r" \draw [color=red]")
    for p in pts:
        if p != pts[-1]:
            print(r"(%f, %f, %f) -- " % (p[0], p[1], p[2]))
        else:
            print(r"(%f, %f, %f);" % (p[0], p[1], p[2]))


def gridFromEnc3D(enc, drawTree=False, showCurve=False, showVirtualLayer=False):
    level = 0
    lctr = [0]
    curvePts = []
    quads = []
    if drawTree:
        treeCode = r"\graph [tree layout, grow=down, fresh nodes, level distance=1.25cm, sibling distance=2cm]"
        treeCode += "\n{\n"

    # function to increment the level counter; includes completion of blocks
    def incrLCtr(l, drawTree):
        nonlocal level
        nonlocal treeCode
        if lctr[l] < 7:
            lctr[l] += 1
        else:
            lctr[l] = 0
            incrLCtr(l - 1, drawTree)
            level -= 1
            if drawTree:
                treeCode += "},\n" if level >= 1 else "}\n"

    # process encoding and draw child cells (i.e. all unrefined cells)
    if enc == '0':
        quad3D([0, 0, 0], [1, 1, 1])
    else:
        for c in enc:
            if c == '1':
                level += 1
                if len(lctr) < level + 1:
                    lctr.append(0)
                if drawTree:
                    treeCode += "\"$\\circ$\" -> {\n"
            else:
                pos = [[0, 0, 0], [1, 1, 1]]
                if showCurve:
                    crv = [0, 0, 0]
                if len(lctr) < level:
                    lctr.append(0)
                for i in range(level + 1):
                    # x direction
                    if lctr[i] % 2 == 1:
                        pos[0][0] += 1. / float(1 << i)
                    # y direction
                    if lctr[i] in [2, 3, 6, 7]:
                        pos[0][1] += 1. / float(1 << i)
                    # z direction
                    if lctr[i] > 3:
                        pos[0][2] += 1. / float(1 << i)
                pos[1][0] = pos[0][0] + 1. / float(1 << level)
                pos[1][1] = pos[0][1] + 1. / float(1 << level)
                pos[1][2] = pos[0][2] + 1. / float(1 << level)
                quads.append(pos)
                if showCurve:
                    crv[0] = pos[0][0] + 1. / float(1 << (level + 1))
                    crv[1] = pos[0][1] + 1. / float(1 << (level + 1))
                    crv[2] = pos[0][2] + 1. / float(1 << (level + 1))
                    curvePts.append(crv)
                if drawTree:
                    treeCode += "\"$\\circ$\",\n" if lctr[level] < 7 else "\"$\\circ$\"\n"
                incrLCtr(level, drawTree)
        if drawTree:
            treeCode += "\n};\n"

        for q in quads:
            quad3D(q[0], q[1])
        if showCurve:
            drawCurve3D(curvePts)
        if drawTree:
            print(r"\begin{scope}")
            print(
                r"\pgftransformcm{%f}{0}{0}{%f}{\pgfpoint{6 cm}{1 cm}}" %
                (1. / len(lctr), 1. / len(lctr)))
            print(treeCode)
            print(r"\end{scope}")


def generateRefinementState2D(enc, parentLevel, lmax):
    for i in range(4):
        # throw the dice about the refinement status of a node if we are not in the last level
        if parentLevel != lmax - 1:
            refStatus = np.random.random_integers(0, 1)
        else:
            refStatus = 0

        # append generated status to encoding string
        enc += str(refStatus)

        # if cell was refined, we have to generate child cells
        if refStatus == 1:
            enc = generateRefinementState2D(enc, parentLevel + 1, lmax)
    return enc


def generateRefinementState3D(enc, parentLevel, lmax):
    for i in range(8):
        # throw the dice about the refinement status of a node if we are not in the last level
        if parentLevel != lmax - 1:
            refStatus = np.random.random_integers(0, 1)
        else:
            refStatus = 0

        # append generated status to encoding string
        enc += str(refStatus)

        # if cell was refined, we have to generate child cells
        if refStatus == 1:
            enc = generateRefinementState3D(enc, parentLevel + 1, lmax)
    return enc


def generateEncoding2D(lmax):
    enc = '1'
    enc = generateRefinementState2D(enc, 0, lmax)
    return enc


def generateEncoding3D(lmax):
    enc = '1'
    enc = generateRefinementState3D(enc, 0, lmax)
    return enc


def draw2DCollision(pos, meshWidth, TeXargs=''):
    for i in range(9):
        endPts = [(meshWidth / 3.) * cos((i * pi) / 4.), (meshWidth / 3.) * sin((i * pi) / 4.)]
        print(r"\draw[->, %s] (%f, %f) -- (%f, %f);" %
              (TeXargs,
               pos[0] + endPts[0],
               pos[1] + endPts[1],
               pos[0] + 1. / 10. * endPts[0],
               pos[1] + 1. / 10. * endPts[1]))


def draw2DStream(pos, meshWidth, TeXargs=''):
    for i in range(9):
        endPts = [(meshWidth / 3.) * cos((i * pi) / 4.), (meshWidth / 3.) * sin((i * pi) / 4.)]
        print(r"\draw[->, %s] (%f, %f) -- (%f, %f);" %
              (TeXargs,
               pos[0] + 1. / 10. * endPts[0],
               pos[1] + 1. / 10. * endPts[1],
               pos[0] + endPts[0],
               pos[1] + endPts[1]))


def draw2DAggregationCollision(pos, meshWidth):
    # draw virtual cells
    print(r"\draw[dashed] (%f, %f) -- (%f, %f);" %
          (pos[0] - 0.5 * meshWidth,
           pos[1],
           pos[0] + 0.5 * meshWidth,
           pos[1]))
    print(r"\draw[dashed] (%f, %f) -- (%f, %f);" %
          (pos[0],
           pos[1] - 0.5 * meshWidth,
           pos[0],
           pos[1] + 0.5 * meshWidth))

    # draw original arrows
    draw2DCollision(pos, meshWidth, 'semithick')

    # draw refined populations on top of refined populations
    for xOffset in [-1, 1]:
        for yOffset in [-1, 1]:
            newPos = [pos[0] + 0.25 * xOffset * meshWidth,
                      pos[1] + 0.25 * yOffset * meshWidth]
            draw2DCollision(newPos, meshWidth * 0.5, 'color=gray')


def draw2DAggregationStream(pos, meshWidth):
    # draw virtual cells
    print(r"\draw[dashed] (%f, %f) -- (%f, %f);" %
          (pos[0] - 0.5 * meshWidth,
           pos[1],
           pos[0] + 0.5 * meshWidth,
           pos[1]))
    print(r"\draw[dashed] (%f, %f) -- (%f, %f);" %
          (pos[0],
           pos[1] - 0.5 * meshWidth,
           pos[0],
           pos[1] + 0.5 * meshWidth))

    # draw original arrows
    draw2DStream(pos, meshWidth, 'semithick')

    # draw refined populations on top of refined populations
    for xOffset in [-1, 1]:
        for yOffset in [-1, 1]:
            newPos = [pos[0] + 0.25 * xOffset * meshWidth,
                      pos[1] + 0.25 * yOffset * meshWidth]
            draw2DStream(newPos, meshWidth * 0.5, 'color=gray')


def draw2DDistributionCollision(pos, meshWidth):
    # draw virtual cells
    print(r"\draw[dashed] (%f, %f) -- (%f, %f);" %
          (pos[0] - 0.5 * meshWidth,
           pos[1],
           pos[0] + 0.5 * meshWidth,
           pos[1]))
    print(r"\draw[dashed] (%f, %f) -- (%f, %f);" %
          (pos[0],
           pos[1] - 0.5 * meshWidth,
           pos[0],
           pos[1] + 0.5 * meshWidth))

    # draw refined populations
    for xOffset in [-1, 1]:
        for yOffset in [-1, 1]:
            newPos = [pos[0] + 0.25 * xOffset * meshWidth,
                      pos[1] + 0.25 * yOffset * meshWidth]
            draw2DCollision(newPos, meshWidth * 0.5)

    # draw original arrows on top of refined populations
    draw2DCollision(pos, meshWidth, 'color=gray, semithick')


def draw2DDistributionStream(pos, meshWidth):
    # draw virtual cells
    print(r"\draw[dashed] (%f, %f) -- (%f, %f);" %
          (pos[0] - 0.5 * meshWidth,
           pos[1],
           pos[0] + 0.5 * meshWidth,
           pos[1]))
    print(r"\draw[dashed] (%f, %f) -- (%f, %f);" %
          (pos[0],
           pos[1] - 0.5 * meshWidth,
           pos[0],
           pos[1] + 0.5 * meshWidth))

    # draw refined populations
    for xOffset in [-1, 1]:
        for yOffset in [-1, 1]:
            newPos = [pos[0] + 0.25 * xOffset * meshWidth,
                      pos[1] + 0.25 * yOffset * meshWidth]
            draw2DStream(newPos, meshWidth * 0.5)

    # draw original arrows on top of refined populations
    draw2DStream(pos, meshWidth, 'color=gray, semithick')


if __name__ == '__main__':
    # enc = '1101000000100000101000000'
    enc = generateEncoding2D(3)
    gridFromEnc2D(enc, True, True)
