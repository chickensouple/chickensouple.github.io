---
title: "Circle-Circle Intersection Area"
date: 2021-02-20
draft: true
---

<link rel="stylesheet" href="html/style.css">

# Introduction
<figure display="table">
  <img src="images/main.png" height="320"/>
  <figcaption display="table-caption" caption-side="bottom"><i>Figure 1: Area of intersection shown in orange. </i></figcaption>
</figure>

We look at computing the area of intersection of two circles (see Figure 1). This problem seems like it should be almost trivial. However, there are some corner cases to handle that are not immediately obvious (at least to me). Googling for this has brought me to several partial results that do not account for all the corner cases, so here is hopefully a post that is complete and can be referenced in the future to be able to quickly implement this computation. Hopefully, this post will not <a href="https://xkcd.com/927/" target="_blank"> cause any further confusion</a>.

TODO: add table of contents


# Computing the Intersection Area

There are some easy corner cases with the intersection of two circles:
1. No intersection area, the circles are too far apart
2. One circle is completely inside the other (coincident circles are a special case of this), thus the intersection area is simply the area of the smaller circle.
3. One intersection point, the circles are touching at one point and have no intersection area.


Finally, there is the "normal" case where the circle edges will intersect at two points as depicted in Figure 1. For the normal case we will start by looking at computing the two "caps" as shown in Figure 2.
<figure display="table">
  <img src="images/caps.png" height="320"/>
  <figcaption display="table-caption" caption-side="bottom"><i>Figure 2: The total area will be the sum of the shaded areas. </i></figcaption>
</figure>
Each cap can be computed by subtracting a triangle from the arc area as shown in Figure 3.
<figure display="table">
  <img src="images/caps_subtraction.png" height="320"/>
  <figcaption display="table-caption" caption-side="bottom"><i>Figure 3 </i></figcaption>
</figure>

To do this, we will need to find the length of the chord. To aid in this we will now define some notation.


### Notation
<figure display="table">
  <img src="images/notation.png" height="320"/>
  <figcaption display="table-caption" caption-side="bottom"><i>Figure 4: Notation. </i></figcaption>
</figure>
Figure 4 gives a visual guide to the various geometric quantities we will define. Note that while Figure 4 gives an example of how various geometric quantities can look, the relationships between them can change given different circles. The quantities are defined as follows:

1. Each circle is defined with a center, \\( \vec{p} = (p_x, p_y)\\), and a radius, \\( r \\). We will subscript these variables to denote either circle 1 or circle 2.
2. The distance between the two centers is defined as \\(D = || \vec{p}_1 - \vec{p}_2||_2\\)
3. The line connecting that contains two points at which the circles intersect is known as the radial axis 
4. The intersection of the radial axis and the line connecting the center of the circles is denoted as \\( \vec{c} \\)
5. The distance between \\(\vec{c} \\) and one of the intersection points is denoted as \\(h\\)
6. The distance between \\(\vec{c} \\) and \\(\vec{p}_1\\) is denoted as \\(d_1\\). \\(d_2\\) is similarily defined.

# Summary

# Widgets





