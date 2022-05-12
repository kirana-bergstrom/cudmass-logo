import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# download "Oswald" font here https://fonts.google.com/specimen/Oswald?preview.text_type=custom
# and put Oswald directory in same directory as this script for custom font
import matplotlib.font_manager as fm
prop = fm.FontProperties(fname='Oswald/Oswald-VariableFont_wght.ttf')

# ------------------------
# global variables
# ------------------------
x_min = 0
x_max = 1
y_min = -0.2
y_max = 0.5

x_mid = (x_max - x_min) / 2 + x_min
x_len = x_max - x_min
y_mid = (y_max - y_min) / 2 + y_min
y_len = y_max - y_min

border_width_x = 0.05
border_width_y = (y_len / x_len) * border_width_x
inn_border_width_x = 0.008
inn_border_width_y = (y_len / x_len) * inn_border_width_x

shrink = 0.85 # amount to shrink left mountain by
# ------------------------


def popcorn(depth):
    """Creates a set of (x,y) points for Thomae's / popcorn function
    Popcorn function is defined as
           {0, x irrational
    f(x) = {q, x = r/q rational

    Args:
    ========
      depth : int
          filename to save the resulting logo as

    Returns:
    ========
      rationals : np.array(float)
          numpy array containing rationals up to specified depth
      y : np.array(float)
          numpy array containing f(rationals)
    """
    depth = int(depth)
    if depth < 2:
        print('specify depth >= 2')
        return

    rationals = []
    y = []

    for i in range(2, depth+1):
        for j in range(1, i):
            rationals.append(j / i)
            y.append(1 / i)

    return np.array(rationals), np.array(y)


def add_text(ax, shape, ratio, shift_up, popcorn_color, header_color1, header_color2,
             footer_color1, footer_color2, draw_region, footer_region):
    """Adds the text and text elements (boxes, lines)

    Note: This function is the worst - text boxes are not fun to work with in matplotlib because
    they don't "snap to" the text inside them. Lots of magic numbers and eyeballing. Not very
    modular and will need to be adjusted if any major changes (sizing, font sizing) are made.

    Args:
    ========
    ax : plt axes object
        used to add shapes to plot
    shape : str
        shape of the logo
    ratio : str
        aspect ratio of the logo
    shift_up : float
        vertical shift of drawing
    popcorn_color : str
        color of the ground/popcorn dots
    header_color1 : str
        color of the header text
    header_color2 : str
        color of the header tag
    footer_color1 : str
        color of footer text
    footer_color2 : str
        color of the footer lines/alt text
    draw_region : mpatches patch object
        draw region (inside borders)
    footer_region : mpatches patch object
        region that footer text can use
    """
    # -----------------------------------------
    # header
    # -----------------------------------------
    header = 'CU Denver'

    if shape == 'circle' or shape == 'oval':
        hshift = 0.07
    else:
        hshift = 0.0

    if ratio == '3:2':
        tag_y0 = 0.72
        header_fsize = 52
        tag_width = 2.5/5 + hshift
    elif ratio == '5:4':
        if shape == 'oval':
            tag_y0 = 0.75
        else:
            tag_y0 = 0.725
        header_fsize = 50
        tag_width = 2.75/5 + hshift / 2
    elif ratio == '1:1':
        tag_y0 = 0.75
        if shape == 'circle':
            header_fsize = 42
        else:
            header_fsize = 46
        tag_width = 0.55 + hshift / 1.5
    tag_height = 0.125
    tag_x0 = 0.0

    tag = ax.add_patch(plt.Rectangle((tag_x0,tag_y0), tag_width, tag_height,
                       fill=True, color=header_color2, zorder=6, transform=ax.transAxes))
    tag.set_clip_path(draw_region)

    htext = plt.text(1/3+hshift, tag_y0+tag_height/2-0.01, header, fontproperties=prop,
                     transform=ax.transAxes, size=header_fsize, zorder=8, color=header_color1,
                     ha='center', va='center')

    # -----------------------------------------
    # footer
    # -----------------------------------------
    footer1 = 'Mathematical and Statistical Sciences'
    footer1a = 'Mathematical and Statistical'
    footer1b = 'Sciences'
    footer2 = 'Department of'
    footer3 = 'Est. 1987'

    if shape == 'circle' or shape == 'oval':
        ft_shift = 4
    else:
        ft_shift = 0

    if ratio == '1:1':
        footer_fsize1 = 34
    elif ratio == '5:4':
        if shape == 'oval':
            footer_fsize1 = 38
        else:
            footer_fsize1 = 34
    else:
        if shape == 'oval':
            footer_fsize1 = 34
        else:
            footer_fsize1 = 40
    footer_fsize2 = 20
    footer_fsize3 = 18

    # for the shifted-up versions, the footer is split into two lines
    if shift_up != 0.0:
        # "Department of" and line
        vdist = 0.35
        vdist_data = vdist*(y_len+border_width_y*2)+y_min-border_width_y
        plt.text(0.5, vdist, footer2, fontproperties=prop, size=footer_fsize2, zorder=8,
                 color=footer_color2, va='center', ha='center', transform=ax.transAxes,
                 bbox=dict(facecolor=popcorn_color, edgecolor='none'))
        line = plt.plot([0.0,1.0], [vdist_data, vdist_data], color=footer_color2, zorder=8, linewidth=2)
        line[0].set_clip_path(footer_region)
        vdist = vdist - 0.075
        plt.text(0.5, vdist, footer1a, fontproperties=prop, size=footer_fsize1-ft_shift, zorder=8,
                 color=footer_color1, ha='center', va='center', transform=ax.transAxes)
        vdist = vdist - 0.08
        plt.text(0.5, vdist, footer1b, fontproperties=prop, size=footer_fsize1-ft_shift, zorder=8,
                 color=footer_color1, ha='center', va='center', transform=ax.transAxes)
        # "Est" and line
        vdist = vdist - 0.075
        vdist_data = vdist*(y_len+border_width_y*2)+y_min-border_width_y
        plt.text(0.5, vdist, footer3, fontproperties=prop, size=footer_fsize3, zorder=8,
                 color=footer_color2, va='center', ha='center', transform=ax.transAxes,
                 bbox=dict(facecolor=popcorn_color, edgecolor='none'))
        line = plt.plot([0.0,1.0],[vdist_data,vdist_data], color=footer_color2, zorder=8, linewidth=2)
        line[0].set_clip_path(footer_region)
    else:
        # "Department of" and line
        vdist = 0.29
        vdist_data = vdist*(y_len+border_width_y*2)+y_min-border_width_y
        plt.text(0.5, vdist, footer2, fontproperties=prop, size=footer_fsize2, zorder=8,
                 color=footer_color2, va='center', ha='center', transform=ax.transAxes,
                 bbox=dict(facecolor=popcorn_color, edgecolor='none'))
        line = plt.plot([0.0,1.0],[vdist_data,vdist_data], color=footer_color2, zorder=8, linewidth=2)
        line[0].set_clip_path(footer_region)
        # main part of footer
        vdist = vdist - 0.078
        ftext = plt.text(0.5, vdist, footer1, fontproperties=prop, size=footer_fsize1-ft_shift,
                         zorder=8, color=footer_color1, ha='center', va='center', transform=ax.transAxes)
        # "Est" and line
        vdist = vdist - 0.075
        vdist_data = vdist*(y_len+border_width_y*2)+y_min-border_width_y
        plt.text(0.5, vdist, footer3, fontproperties=prop, size=footer_fsize3, zorder=8,
                 color=footer_color2, va='center', ha='center', transform=ax.transAxes,
                 bbox=dict(facecolor=popcorn_color, edgecolor='none'))
        line = plt.plot([0.0,1.0],[vdist_data,vdist_data], color=footer_color2, zorder=8, linewidth=2)
        line[0].set_clip_path(footer_region)


def draw_sky(ax, shift_up, color, draw_region, dpcs):
    """Draws the sky

    Args:
    ========
    ax : plt axes object
        used to add shapes to plot
    shift_up : float
        vertical shift of drawing
    color : str or list of strings
        hex color(s) or other string color(s) defining the colors in the sky
        if list of strings will be striped from first element at top to last element at bottom
    draw_region : mpatches patch object
        draw region (inside borders)
    """
    if type(color) == str:
        sky = [color]
    else:
        sky = color

    # some adjustments depending on the number of colors. B/c the sky doesn't end at exactly 0,
    # looks better to adjust the heights of the stripes depending on the number.
    if len(sky) == 1:
        denom = len(sky)
        alpha = 1.0
        color = sky[0]
        if sky[0] == 'transparent':
            color = '#FFFFFF'
            alpha = 0.0
        sky = ax.add_patch(plt.Rectangle((0.0,0.0), 1.0, 1.0, alpha=alpha,
                                         facecolor=color, transform=ax.transAxes, zorder=0))
        sky.set_clip_path(draw_region)
    elif len(sky) < 4:
        denom = len(sky) + 0.9 # adjust this number for number of stripes
        height = (1 - shift_up) / denom
        for count, color in enumerate(sky):
            alpha = 1.0
            if color == 'transparent':
                color = '#FFFFFF'
                alpha = 0.0
            sky = ax.add_patch(plt.Rectangle((0.0, 1-(count+1)*height), 1.0, height,
                                             facecolor=color, transform=ax.transAxes, zorder=0, alpha=alpha))
            sky.set_clip_path(draw_region)
    elif len(sky) < 6:
        denom = len(sky) + 1.9 # adjust this number for number of stripes
        height = (1 - shift_up) / denom
        for count, color in enumerate(sky):
            alpha = 1.0
            if color == 'transparent':
                color = '#FFFFFF'
                alpha = 0.0
            sky = ax.add_patch(plt.Rectangle((0.0, 1-(count+1)*height), 1.0, height,
                                             facecolor=color, transform=ax.transAxes, zorder=0, alpha=alpha))
            sky.set_clip_path(draw_region)
    else:
        denom = len(sky) + 2.5
        height = (1 - shift_up) / denom # adjust this number for number of stripes
        for count, color in enumerate(sky):
            alpha = 1.0
            if color == 'transparent':
                color = '#FFFFFF'
                alpha = 0.0
            sky = ax.add_patch(plt.Rectangle((0.0, 1-(count+1)*height), 1.0, height,
                                             facecolor=color, transform=ax.transAxes, zorder=0, alpha=alpha))
            sky.set_clip_path(draw_region)


def draw_popcorn(ax, shift_up, color, draw_region):
    """Draws the dots for the popcorn function

    Args:
    ========
    ax : plt axes object
        used to add shapes to plot
    shift_up : float
        vertical shift of drawing
    color : str
        hex color or other string color defining the color of the dots
    draw_region : mpatches patch object
        draw region (inside borders)
    """
    x, y = popcorn(110)
    y[(x <= 0.5)] = y[(x <= 0.5)] * shrink

    # note: we don't plot the top middle dot since it doesn't become a part of either mountain
    dots = ax.scatter(x[1:], y[1:]+shift_up, color=color, s=50, zorder=5)
    dots.set_clip_path(draw_region)

    # fill area below, add extra bit (0.01) to the height to cover gap between dots and ground
    dots_patch = ax.add_patch(mpatches.Rectangle((x_min,y_min), x_max-x_min,
                                                 np.abs(y_min)+0.01+shift_up,
                                                 fill=True, color=color, linewidth=2, zorder=5))
    dots_patch.set_clip_path(draw_region)


def draw_mountains(ax, shift_up, color_1, color_2, draw_region, dpcs):
    """Draws the mountains

    Note: a lot of "magic" numbers here, but all correspond to a popcorn function point.
    Can be changed to change shape/shading of mountains

    Args:
    ========
    ax : plt axes object
        used to add shapes to plot
    shift_up : float
        vertical shift of drawing
    color_1 : str
        hex color or other string color defining the edge color of mountains
    color_2 : str
        hex color or other string color defining the inner/snow color of mountains
    draw_region : mpatches patch object
        draw region (inside borders)
    """
    alpha = 1.0
    if color_2 == 'transparent':
        alpha = 0.0
        color_2 = '#FFFFFF'
    # right mountain
    mp = plt.plot([0.5,2/3],[0+shift_up,1/3+shift_up], color=color_1, zorder=4, linewidth=3)
    mp[0].set_clip_path(draw_region)
    mountain = ax.add_patch(plt.Polygon([[2/3,1/3+shift_up],
                                         [4/6,1/6+shift_up],
                                         [1,0+shift_up]
                                        ], closed=True, fill=True, color=color_1, zorder=4))
    mountain.set_clip_path(draw_region)
    mountain = ax.add_patch(plt.Polygon([[5/8,1/8+shift_up],
                                         [4/6,1/6+shift_up],
                                         [2/3,1/3+shift_up]
                                        ], closed=True, fill=True, color=color_1, zorder=4))
    mountain.set_clip_path(draw_region)
    mountain = ax.add_patch(plt.Polygon([[1/2,0+shift_up],
                                         [21/40,1/40+shift_up],
                                         [2/3,1/3+shift_up]
                                        ], closed=True, fill=True, color=color_1, zorder=4))
    mountain.set_clip_path(draw_region)
    mountain = ax.add_patch(plt.Polygon([[1/2,0+shift_up],
                                         [2/3,1/3+shift_up],
                                         [1,0+shift_up]
                                        ], closed=True, fill=True, color=color_2, alpha=alpha, zorder=3))
    mountain.set_clip_path(draw_region)

    # left mountain
    mp = plt.plot([0,1/3],[0+shift_up,1/3*shrink+shift_up], color=color_1, zorder=2, linewidth=3)
    mp[0].set_clip_path(draw_region)
    mp = plt.plot([1/3,3/5],[1/3*shrink+shift_up,1/5*shrink+shift_up],
                  color=color_1, zorder=2, linewidth=3)
    mp[0].set_clip_path(draw_region)
    mountain = ax.add_patch(plt.Polygon([[1/3,1/3*shrink+shift_up],
                                         [1/2,0+shift_up],
                                         [3/5,1/5*shrink+shift_up]
                                        ], closed=True, fill=True, color=color_1, zorder=2))
    mountain.set_clip_path(draw_region)
    mountain = ax.add_patch(plt.Polygon([[1/3,1/3*shrink+shift_up],
                                         [2/7,1/7*shrink+shift_up],
                                         [2/5,1/5*shrink+shift_up]
                                        ], closed=True, fill=True, color=color_1, zorder=2))
    mountain.set_clip_path(draw_region)
    mountain = ax.add_patch(plt.Polygon([[2/6,1/6*shrink+shift_up],
                                         [5/15,1/15*shrink+shift_up],
                                         [4/9,1/9*shrink+shift_up],
                                         [2/5,1/5*shrink+shift_up]
                                        ], closed=True, fill=True, color=color_1, zorder=2))
    mountain.set_clip_path(draw_region)
    mountain = ax.add_patch(plt.Polygon([[1/3,1/3*shrink+shift_up],
                                         [0/15,0/15*shrink+shift_up],
                                         [2/30,1/30*shrink+shift_up]
                                        ], closed=True, fill=True, color=color_1, zorder=2))
    mountain.set_clip_path(draw_region)
    mountain = ax.add_patch(plt.Polygon([[0,0+shift_up],
                                         [1/3,1/3*shrink+shift_up],
                                         [1/2,0+shift_up]
                                        ], closed=True, fill=True, color=color_2, zorder=1, alpha=alpha))
    mountain.set_clip_path(draw_region)


def background_shapes(ax, shape, ratio, color_border1, color_border2):
    """Creates the background shapes
    The background shapes define the borders of the logo

    Args:
    ========
    ax : plt axes object
        used to add shapes to plot
    shape : str
        defines the shape of the logo
    ratio : str
        aspect ratio of the logo
    color_border1 : str
        hex color or other string color defining the border color
    color_border2 : str
        hex color or other string color defining the contrasting border color
    """
    if ratio == '3:2':
        scale_x_bw = 2 / 3
    elif ratio == '5:4':
        scale_x_bw = 4 / 5
    else:
        scale_x_bw = 1

    width_x = (border_width_x - inn_border_width_x) / 2
    width_y = (border_width_y - inn_border_width_y) / 2

    swidth_x = width_x*scale_x_bw
    sinn_border_width_x = inn_border_width_x*scale_x_bw
    sborder_width_x = border_width_x*scale_x_bw
    
    dpcs = []

    if shape == 'circle' or shape == 'oval':
        # defines an extra patch to cut the footer off at horizontal edges
        footer_region = ax.add_patch(mpatches.Ellipse((x_mid, y_mid),
                                                      x_len-4*swidth_x, y_len-2*width_y,
                                                      fill=False, color='#FFFFFF', alpha=0.0))
        # defines the region inside the border
        draw_region = ax.add_patch(mpatches.Ellipse((x_mid, y_mid),
                                                    x_len, y_len,
                                                    fill=False, linewidth=2,
                                                    color=color_border1, zorder=10))
        # first inner border
        border1_region = ax.add_patch(mpatches.Ellipse((x_mid, y_mid),
                                                       x_len+2*swidth_x, y_len+2*width_y,
                                                       fill=True, color=color_border1, zorder=0))
        # second (contrasting color) border
        border2_region = ax.add_patch(mpatches.Ellipse((x_mid, y_mid),
                                                       x_len+2*swidth_x+2*sinn_border_width_x,
                                                       y_len+2*width_y+2*inn_border_width_y,
                                                       fill=True, color=color_border2, zorder=-1))
        # final outside border
        border3_region = ax.add_patch(mpatches.Ellipse((x_mid, y_mid),
                                                       x_len+2*sborder_width_x,
                                                       y_len+2*border_width_y,
                                                       fill=True, color=color_border1, zorder=-2))
    elif shape == 'rectangle' or shape == 'square':
        # defines an extra patch to cut the footer off at horizontal edges
        footer_region = ax.add_patch(mpatches.Rectangle((x_min+2*swidth_x, y_min+width_y),
                                                        x_len-4*swidth_x, y_len-2*width_y,
                                                        fill=False, color='#FFFFFF', alpha=0.0))
        # defines the region inside the border
        draw_region = ax.add_patch(mpatches.Rectangle((x_min, y_min),
                                                      x_len, y_len,
                                                      color=color_border1, fill=False,
                                                      zorder=10, linewidth=2))
        # first inner border
        border1_region = ax.add_patch(mpatches.Rectangle((x_min-swidth_x, y_min-width_y),
                                                         x_len+2*swidth_x,
                                                         y_len+2*width_y,
                                                         fill=True, color=color_border1, zorder=0))
        # second (contrasting color) border
        border2_region = ax.add_patch(mpatches.Rectangle((x_min-swidth_x-sinn_border_width_x,
                                                          y_min-width_y-inn_border_width_y),
                                                         x_len+2*swidth_x+2*sinn_border_width_x,
                                                         y_len+2*width_y+2*inn_border_width_y,
                                                         fill=True, color=color_border2,
                                                         zorder=-1))
        # final outside border
        border3_region = ax.add_patch(mpatches.Rectangle((x_min-sborder_width_x,
                                                          y_min-border_width_y),
                                                         x_len+2*sborder_width_x,
                                                         y_len+2*border_width_y,
                                                         fill=True, color=color_border1,
                                                         zorder=-2))
    elif shape == 'rounded_rectangle' or shape == 'rounded_square':

        p = 0.09 # padding for rounding
        
        # defines an extra patch to cut the footer off at horizontal edges
        footer_region = ax.add_patch(mpatches.FancyBboxPatch((x_min+2*swidth_x+p, y_min+width_y+p),
                                                             x_len-4*swidth_x-2*p, y_len-2*width_y-2*p,
                                                             boxstyle=mpatches.BoxStyle("Round", pad=p),
                                                             fill=False, color='#FFFFFF', alpha=0.0))
        # defines the region inside the border
        draw_region = ax.add_patch(mpatches.FancyBboxPatch((x_min+p, y_min+p),
                                                           x_len-2*p, y_len-2*p,
                                                           boxstyle=mpatches.BoxStyle("Round", pad=p),
                                                           color=color_border1, fill=False,
                                                           zorder=10, linewidth=2))
        # first inner border
        border1_region = ax.add_patch(mpatches.FancyBboxPatch((x_min-swidth_x+p, y_min-width_y+p),
                                                              x_len+2*swidth_x-2*p,
                                                              y_len+2*width_y-2*p,
                                                              boxstyle=mpatches.BoxStyle("Round", pad=p),
                                                              fill=True, color=color_border1, zorder=0))
        # second (contrasting color) border
        border2_region = ax.add_patch(mpatches.FancyBboxPatch((x_min-swidth_x-sinn_border_width_x+p,
                                                               y_min-width_y-inn_border_width_y+p),
                                                              x_len+2*swidth_x+2*sinn_border_width_x-2*p,
                                                              y_len+2*width_y+2*inn_border_width_y-2*p,
                                                              boxstyle=mpatches.BoxStyle("Round", pad=p),
                                                              fill=True, color=color_border2,
                                                              zorder=-1))
        # final outside border
        border3_region = ax.add_patch(mpatches.FancyBboxPatch((x_min-sborder_width_x+p,
                                                               y_min-border_width_y+p),
                                                              x_len+2*sborder_width_x-2*p,
                                                              y_len+2*border_width_y-2*p,
                                                              boxstyle=mpatches.BoxStyle("Round", pad=p),
                                                              fill=True, color=color_border1,
                                                              zorder=-2, ec='none'))
    else:
        # slope of the parabola defining the upper/lower edges changes with aspect ratio
        if ratio == '3:2':
            par_slope = 0.3
        elif ratio == '5:4':
            par_slope = 0.2
        else:
            par_slope = 0.15
        # defines an extra patch to cut the footer off at horizontal edges
        xx = np.linspace(x_min+2*swidth_x, x_max-2*swidth_x, 1000)
        footer_patch = plt.fill_between(xx,
                                        par_slope*(xx-0.5)**2+y_min+width_y,
                                        -par_slope*(xx-0.5)**2+y_max-width_y,
                                        color='#FFFFFF', alpha=0.0)
        path_footer, = footer_patch.get_paths()
        footer_region = mpatches.PathPatch(path_footer, fc='none', ec='none')
        ax.add_patch(footer_region)
        # defines the region inside the border
        xx = np.linspace(x_min, x_max, 1000)
        draw_patch = plt.fill_between(xx,
                                      par_slope*(xx-0.5)**2+y_min,
                                      -par_slope*(xx-0.5)**2+y_max,
                                      color=color_border1, alpha=0.0)
        path_draw, = draw_patch.get_paths()
        draw_region = mpatches.PathPatch(path_draw, fc='none', ec=color_border1, linewidth=2, zorder=10)
        ax.add_patch(draw_region)
        # -----------------------------
        draw_patch_complement = plt.fill_between(xx,
                                                 par_slope*(xx-0.5)**2+y_min,
                                                 y_min-0.2,
                                                 color='none', alpha=1.0, zorder=100)
        path_draw, = draw_patch_complement.get_paths()
        draw_region_complement = mpatches.PathPatch(path_draw,
                                                    fc='none',
                                                    ec='none',
                                                    linewidth=2, zorder=10)
        ax.add_patch(draw_region_complement)
        dpcs.append(draw_region_complement)
        draw_patch_complement = plt.fill_between(xx,
                                                 y_max+0.2,
                                                 -par_slope*(xx-0.5)**2+y_max,
                                                 color='none', alpha=1.0, zorder=100)
        path_draw, = draw_patch_complement.get_paths()
        draw_region_complement = mpatches.PathPatch(path_draw,
                                                    fc='none',
                                                    ec='none',
                                                    linewidth=2, zorder=10)
        ax.add_patch(draw_region_complement)
        dpcs.append(draw_region_complement)
        xx = np.linspace(x_min-0.2, x_min, 1000)
        draw_patch_complement = plt.fill_between(xx,
                                                 y_min-0.2,
                                                 y_max+0.2,
                                                 color='none', alpha=1.0, zorder=100)
        path_draw, = draw_patch_complement.get_paths()
        draw_region_complement = mpatches.PathPatch(path_draw,
                                                    fc='none',
                                                    ec='none',
                                                    linewidth=2, zorder=10)
        ax.add_patch(draw_region_complement)
        dpcs.append(draw_region_complement)
        xx = np.linspace(x_max, x_max+0.2, 1000)
        draw_patch_complement = plt.fill_between(xx,
                                                 y_min-0.2,
                                                 y_max+0.2,
                                                 color='none', alpha=1.0, zorder=100)
        path_draw, = draw_patch_complement.get_paths()
        draw_region_complement = mpatches.PathPatch(path_draw,
                                                    fc='none',
                                                    ec='none',
                                                    linewidth=2, zorder=10)
        ax.add_patch(draw_region_complement)
        dpcs.append(draw_region_complement)
        # -----------------------------
        # first inner border
        xx = np.linspace(x_min-swidth_x, x_max+swidth_x, 1000)
        for p in dpcs:
            border1_region = plt.fill_between(xx,
                                              par_slope*(xx-0.5)**2+y_min-width_y,
                                              -par_slope*(xx-0.5)**2+y_max+width_y,
                                              color=color_border1, zorder=0)
            border1_region.set_clip_path(p)
        # second (contrasting color) border
        xx = np.linspace(x_min-swidth_x-sinn_border_width_x,
                         x_max+swidth_x+sinn_border_width_x,
                         1000)
        for p in dpcs:
            border2_region = plt.fill_between(xx,
                                              par_slope*(xx-0.5)**2+y_min-width_y-inn_border_width_y,
                                              -par_slope*(xx-0.5)**2+y_max+width_y+inn_border_width_y,
                                              color=color_border2, zorder=-1)
            border2_region.set_clip_path(p)
        # final outside border
        xx = np.linspace(x_min-sborder_width_x, x_max+sborder_width_x, 1000)
        for p in dpcs:
            border3_region = plt.fill_between(xx,
                                              par_slope*(xx-0.5)**2+y_min-border_width_y,
                                              -par_slope*(xx-0.5)**2+y_max+border_width_y,
                                              color=color_border1, zorder=-2)
            border3_region.set_clip_path(p)

    return draw_region, footer_region, dpcs


def logo(fname, colors, ratio='5:4', shape='default'):
    """Creates and saves the logo

    Args:
    ========
      fname : str
          filename to save the resulting logo as
      colors : dict of str
          defines hex colors for logo features
          popcorn        - dots that make up the popcorn function
          mountains_edge - edges/triangles of the mountains
          mountains_snow - "snowy" part of the mountains
          edge           - border of the logo
          header_tag     - "tag" behind the "CU Denver" header
          header_text    - text of the header
          footer_lines   - lines and text surrounding the "Department of..." footer
          footer_text    - "Department of..." footer text
          sky            - sky, can be a single color or a list of colors for stripes.
                           >7 stripes may require adjusting the code so all stripes can be seen
      ratio : str, default='3:2'
          sets the ratio of the logo, valid ratios are '3:2', '5:4', '1:1'
      shape : str, default='default'
          sets the shape of the logo
          default is straight vertical edges, parabolic upper/lower
          other valid shapes are: rectangle, square (1:1 rectangle), oval, circle (1:1 oval)
    """
    # -----------------------------------
    # argument checking
    # -----------------------------------
    if shape not in ['square', 'circle', 'default', 'rectangle', 'oval', 'rounded_rectangle', 'rounded_square']:
        print('shape is not valid!')
        print('Please use shape=\'square\', \'rectangle\', \'circle\', \'oval\', \'rounded_rectangle\', \'rounded_square\' or \'default\'')
        return
    if ratio not in ['3:2', '5:4', '1:1']:
        print('ratio is not valid!')
        print('Please use ratio=\'3:2\', ratio=\'5:4\', or ratio=\'1:1\'')
        return

    ftype = fname.split('.')[1]
    if ftype != 'png' and ftype != 'eps':
        print('file type can only be png or eps!')
        return

    # square is a 1:1 rectangle, circle is a 1:1 oval, just force it
    if shape == 'square' or shape == 'circle' or shape == 'rounded_square':
        ratio = '1:1'
    if shape == 'oval' and ratio == '1:1':
        shape = 'circle'
    if shape == 'rectangle' and ratio == '1:1':
        shape = 'square'

    # the whole logo gets shifted up for a 1:1 ratio, or a 5:4 oval
    if ratio == '1:1' or (ratio == '5:4' and shape == 'oval'):
        shift_up = 0.04
    else:
        shift_up = 0.0


    # -----------------------------------
    # begin plotting
    # -----------------------------------
    ax = plt.gca() # set up axis
    fig = plt.gcf() # set up fig

    draw_region, footer_region, dpcs = background_shapes(ax, shape, ratio,
                                                         colors['border'], colors['border_contrast'])

    draw_mountains(ax, shift_up, colors['mountains_edge'], colors['mountains_snow'], draw_region, dpcs)

    draw_popcorn(ax, shift_up, colors['popcorn'], draw_region)

    draw_sky(ax, shift_up, colors['sky'], draw_region, dpcs)

    add_text(ax, shape, ratio, shift_up,
             colors['popcorn'], colors['header_text'], colors['header_tag'],
             colors['footer_text'], colors['footer_lines'], draw_region, footer_region)

    # remove axes
    ax.axis('off')

    # stretch axes
    if ratio == '3:2':
        scale_x_bw = 2 / 3
    elif ratio == '5:4':
        scale_x_bw = 4 / 5
    else:
        scale_x_bw = 1

    width_x = (border_width_x - inn_border_width_x) / 2
    width_y = (border_width_y - inn_border_width_y) / 2

    swidth_x = width_x*scale_x_bw
    sinn_border_width_x = inn_border_width_x*scale_x_bw
    sborder_width_x = border_width_x*scale_x_bw
    
    plt.xlim(x_min-sborder_width_x-sinn_border_width_x, x_max+sborder_width_x+sinn_border_width_x)
    plt.ylim(y_min-border_width_y-inn_border_width_y, y_max+border_width_y+inn_border_width_y)

    # set size
    if ratio == '3:2':
        fig.set_size_inches(12, 8)
    elif ratio == '5:4':
        fig.set_size_inches(10, 8)
    elif ratio == '1:1':
        fig.set_size_inches(8, 8)

    # check if images directory exists
    im_dir_exists = os.path.exists('images')
    if not im_dir_exists:
        os.mkdir('images')

    # save
    if ftype == 'eps':
        fig.savefig('images/'+fname, transparent=True, pad_inches=0.25, format='eps', dpi=1200)
    else:
        fig.savefig('images/'+fname, transparent=True, pad_inches=0.25, dpi=1200)
