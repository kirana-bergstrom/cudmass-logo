import logo

import matplotlib.pyplot as plt
import os

import matplotlib.font_manager as fm
prop = fm.FontProperties(fname='Bungee_Inline/BungeeInline-Regular.ttf')
prop2 = fm.FontProperties(fname='Yellowtail/Yellowtail-Regular.ttf')


def add_text(ax, shape, ratio, shift_up, popcorn_color, header_color1, header_color2,
             footer_color1, footer_color2, footer_color3, draw_region, footer_region):
    """
    Adds the text and text elements (boxes, lines)

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

    # for circular shapes, we shift the header text over a bit so it doesn't run into the border
    if shape == 'circle' or shape == 'oval':
        hshift = 0.07
    else:
        hshift = 0.0

    # sets specific sizes for each ratio/shape
    if ratio == '3:2':
        tag_y0 = 0.72
        header_fsize = 56
        tag_width = 2.5/5 + hshift
    elif ratio == '5:4':
        if shape == 'oval':
            tag_y0 = 0.75
        else:
            tag_y0 = 0.725
        header_fsize = 54
        tag_width = 2.75/5 + hshift / 2
    elif ratio == '3:1':
        if shape == 'oval':
            tag_y0 = 0.75
        else:
            tag_y0 = 0.725
        header_fsize = 56
        tag_width = 2.25/5 + hshift / 2
    elif ratio == '1:1':
        tag_y0 = 0.75
        if shape == 'circle':
            header_fsize = 46
        else:
            header_fsize = 48
        tag_width = 0.55 + hshift / 1.5

    tag_height = 0.125
    tag_x0 = 0.0

    start_height = tag_y0+1.25*tag_height/2.25
    tag = ax.add_patch(plt.Rectangle((tag_x0,start_height), tag_width, tag_height/2.25,
                       fill=True, color=header_color2, zorder=6, transform=ax.transAxes))
    tag.set_clip_path(draw_region)
    gap = 0.0075
    start_height = start_height - gap - tag_height/8
    tag2 = ax.add_patch(plt.Rectangle((tag_x0,start_height), tag_width, tag_height/8,
                       fill=True, color=header_color2, zorder=6, transform=ax.transAxes))
    tag2.set_clip_path(draw_region)
    start_height = start_height - gap - tag_height/8
    tag3 = ax.add_patch(plt.Rectangle((tag_x0,start_height), tag_width, tag_height/8,
                       fill=True, color=header_color2, zorder=6, transform=ax.transAxes))
    tag3.set_clip_path(draw_region)
    start_height = start_height - gap - tag_height/8
    tag4 = ax.add_patch(plt.Rectangle((tag_x0,start_height), tag_width, tag_height/8,
                       fill=True, color=header_color2, zorder=6, transform=ax.transAxes))
    tag4.set_clip_path(draw_region)

    htext = plt.text(1/3+hshift, tag_y0+tag_height/2-0.01, header, fontproperties=prop2, rotation=15,
                     transform=ax.transAxes, size=header_fsize, zorder=8, color=header_color1,
                     ha='center', va='center')

    # -----------------------------------------
    # footer
    # -----------------------------------------
    footer1 = 'Math and Stats Club'
    footer1a = 'Math and'
    footer1b = 'Stats Club'
    footer2 = 'Department of Mathematical'
    footer3 = 'and Statistical Sciences'

    if shape == 'circle' or shape == 'oval':
        ft_shift = 4
    else:
        ft_shift = 0

    if ratio == '5:4':
        if shape == 'oval':
            footer_fsize1 = 36
        else:
            footer_fsize1 = 38
    elif ratio == '1:1':
        if shape == 'circle':
            footer_fsize1 = 30
        else:
            footer_fsize1 = 36
    elif ratio == '3:2':
        if shape == 'oval':
            footer_fsize1 = 38
        else:
            footer_fsize1 = 46 # check
    elif ratio == '3:1':
        footer_fsize1 = 48
    footer_fsize2 = 16
    footer_fsize3 = 16
    
    # for the shifted-up versions, the footer is split into two lines
    if 0.0 != 0.0:
        # "Department of Mathematical" and line
        vdist = 0.45
        vdist_data = vdist*(logo.y_len+logo.border_width_y*2)+logo.y_min-logo.border_width_y
        plt.text(0.15, vdist, footer2, fontproperties=logo.prop, size=footer_fsize2, zorder=8,
                 color=footer_color2, va='center', ha='left', transform=ax.transAxes,
                 bbox=dict(facecolor=popcorn_color, edgecolor='none'))
        #line = plt.plot([0.0,1.0], [vdist_data, vdist_data],
                        #color=footer_color3, zorder=8, linewidth=2)
        #line[0].set_clip_path(footer_region)
        vdist = vdist - 0.075
        plt.text(0.5, vdist, footer1a, fontproperties=logo.prop, size=(footer_fsize1-ft_shift),
                 zorder=8, color=footer_color1, ha='center', va='center', transform=ax.transAxes)
        vdist = vdist - 0.08
        plt.text(0.5, vdist, footer1b, fontproperties=logo.prop, size=(footer_fsize1-ft_shift),
                 zorder=8, color=footer_color1, ha='center', va='center', transform=ax.transAxes)
        # "and Statistical Sciences" and line
        vdist = vdist - 0.075
        vdist_data = vdist*(logo.y_len+logo.border_width_y*2)+logo.y_min-logo.border_width_y
        plt.text(0.85, vdist, footer3, fontproperties=logo.prop, size=(footer_fsize3), zorder=8,
                 color=footer_color2, va='center', ha='right', transform=ax.transAxes,
                 bbox=dict(facecolor=popcorn_color, edgecolor='none'))
        #line = plt.plot([0.0,1.0],[vdist_data,vdist_data],
                        #color=footer_color2, zorder=8, linewidth=2)
        #line[0].set_clip_path(footer_region)
    else:
        # need to shift down a little for banner size
        vshift = 0.05 if shift_up != 0 else 0.0
        # "Department of Mathematical" and line
        vdist = 0.3 + vshift
        vdist_data = vdist*(logo.y_len+logo.border_width_y*2)+logo.y_min-logo.border_width_y
        if shape == 'oval' or shape == 'circle':
            if ratio == '1:1':
                lower_line_scale = 1.5
            elif ratio == '5:4':
                lower_line_scale = 1.75
            else:
                lower_line_scale = 2
        else:
            lower_line_scale = 1.0
        if ratio == '3:1':
            end_line_frac = 0.3
        elif ratio == '5:4' or ratio == '3:2':
            end_line_frac = 0.15
        elif ratio == '1:1':
            end_line_frac = 0.2
        plt.text(end_line_frac, vdist, footer2, fontproperties=prop2, size=footer_fsize2, zorder=8,
                 color=footer_color3, va='center', ha='left', transform=ax.transAxes,
                 bbox=dict(facecolor=popcorn_color, edgecolor='none'))
        
        #line = plt.plot([0.0,1.0], [vdist_data,vdist_data],
                        #color=footer_color2, zorder=8, linewidth=3)
        #line[0].set_clip_path(footer_region)
        line = plt.plot([0.0,1.0], [vdist_data-0.02,vdist_data-0.02],
                color=footer_color2, zorder=9, linewidth=3)
        line[0].set_clip_path(footer_region)
        # main part of footer
        vdist = vdist - 0.075 #+ vshift
        vdist_data = vdist*(logo.y_len+logo.border_width_y*2)+logo.y_min-logo.border_width_y
        if ratio != '1:1' or shape == 'circle':
            ftext = plt.text(0.5, vdist, footer1, fontproperties=prop, size=(footer_fsize1-ft_shift),
                             zorder=9, color=footer_color1, ha='center', va='center',
                             transform=ax.transAxes)
        else:
            ftext = plt.text(0.5, vdist, footer1a, fontproperties=prop, size=(footer_fsize1-ft_shift),
                             zorder=9, color=footer_color1, ha='center', va='center',
                             transform=ax.transAxes)
            vdist = vdist - 0.08
            vdist_data = vdist*(logo.y_len+logo.border_width_y*2)+logo.y_min-logo.border_width_y
            plt.text(0.5, vdist, footer1b, fontproperties=prop, size=(footer_fsize1-ft_shift),
                 zorder=8, color=footer_color1, ha='center', va='center', transform=ax.transAxes)

        # "and Statistcal Sciences" and line
        vdist = vdist - 0.082 #+ vshift
        vdist_data = vdist*(logo.y_len+logo.border_width_y*2)+logo.y_min-logo.border_width_y
        line = plt.plot([0.0,1.0], [vdist_data+0.02,vdist_data+0.02],
                        color=footer_color2, zorder=9, linewidth=3)
        line[0].set_clip_path(footer_region)
        
        plt.text(1-end_line_frac*lower_line_scale, vdist, footer3, fontproperties=prop2, size=footer_fsize3, zorder=8,
                 color=footer_color3, va='center', ha='right', transform=ax.transAxes,
                 bbox=dict(facecolor=popcorn_color, edgecolor='none'))
        #line = plt.plot([0.0,1.0],[vdist_data,vdist_data], color=footer_color2, zorder=8, linewidth=3)
        #line[0].set_clip_path(footer_region)


def logo_mathstats(fname, colors, ratio='5:4', shape='default',
                       dpi=1200, marker='o', ftype='png'):
    """
    Creates and saves the logo

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
      dpi : int, default=1200
          sets the dots-per-inch for image
          default is 1200, high res
      marker : str, default='o'
          sets the shape of the popcorn function markers
          default is 'o', circles
          other valid markers are '*', others are untested
      ftype : str, default='png'
          sets the filetype for the image
          default is png
          other valid filetypes are 'svg' and 'eps'
    """
    # -----------------------------------
    # argument checking
    # -----------------------------------
    if shape not in ['square', 'circle', 'default', 'rectangle',
                     'oval', 'rounded_rectangle', 'rounded_square']:
        print('ERROR: shape is not valid!')
        print('Please use shape=\'square\', \'rectangle\', \'circle\', \'oval\', \'rounded_rectangle\', \'rounded_square\' or \'default\'')
        return
    if ratio not in ['3:2', '5:4', '1:1', '3:1']:
        print('ERROR: ratio is not valid!')
        print('Please use ratio=\'3:2\', ratio=\'5:4\', ratio=\'3:1\', or ratio=\'1:1\'')
        return
    if ratio == '3:1' and shape != 'rectangle':
        print('ERROR: shape and ratio combo is not valid!')
        print('3:1 ratio is banner size and cannot be used with shapes other than \'rectangle\'')
        return

    # only 'png', 'eps', and 'svg' will work for file types
    if ftype not in ['eps', 'png', 'svg']:
        print('ERROR: only eps, png, and svg filetypes are accepted')
        return

    # square is a 1:1 rectangle, circle is a 1:1 oval, just force it
    if shape == 'square' or shape == 'circle' or shape == 'rounded_square':
        ratio = '1:1'
    if shape == 'oval' and ratio == '1:1':
        shape = 'circle'
    if shape == 'rectangle' and ratio == '1:1':
        shape = 'square'

    # only 'png', 'eps', and 'svg' will work for file types
    if fname.split('.')[1] != ftype:
        print('WARNING: generally the filetype should be the same as the file extension')

    # the whole logo gets shifted up for a 1:1 ratio, or a 5:4 oval
    if ratio == '1:1' or (ratio == '5:4' and shape == 'oval') or (ratio == '3:1' and shape == 'oval'):
        shift_up = 0.04
    else:
        shift_up = 0.0

    # -----------------------------------
    # begin plotting
    # -----------------------------------
    plt.figure()
    ax = plt.gca() # set up axis
    fig = plt.gcf() # set up fig

    draw_region, footer_region = logo.background_shapes(ax, shape, ratio,
                                                   colors['border'], colors['border_contrast'])

    logo.draw_mountains(ax, ratio, shift_up, colors['mountains_edge'], colors['mountains_snow'], draw_region)

    logo.draw_popcorn(ax, ratio, shift_up, colors['popcorn'], marker, draw_region)

    logo.draw_sky(ax, shift_up, colors['sky'], draw_region)

    add_text(ax, shape, ratio, shift_up,
             colors['popcorn'], colors['header_text'], colors['header_tag'],
             colors['footer_text'], colors['footer_lines'], colors['footer_small_text'], draw_region, footer_region)

    # remove axes
    ax.axis('off')

    # stretch axes
    if ratio == '3:2':
        scale_x_bw = 2 / 3
    elif ratio == '5:4':
        scale_x_bw = 4 / 5
    elif ratio == '3:1':
        scale_x_bw = 1 / 3
    else:
        scale_x_bw = 1

    # set x and y limits, including borders
    width_x = (logo.border_width_x - logo.inn_border_width_x) / 2
    width_y = (logo.border_width_y - logo.inn_border_width_y) / 2

    swidth_x = width_x*scale_x_bw
    sinn_border_width_x = logo.inn_border_width_x*scale_x_bw
    sborder_width_x = logo.border_width_x*scale_x_bw
    
    plt.xlim(logo.x_min-sborder_width_x-sinn_border_width_x, logo.x_max+sborder_width_x+sinn_border_width_x)
    plt.ylim(logo.y_min-logo.border_width_y-logo.inn_border_width_y, logo.y_max+logo.border_width_y+logo.inn_border_width_y)

    # set size
    if ratio == '3:2':
        fig.set_size_inches(9, 6, forward=True)
    elif ratio == '5:4':
        fig.set_size_inches(7.5, 6, forward=True)
    elif ratio == '1:1':
        fig.set_size_inches(6, 6, forward=True)
    elif ratio == '3:1':
        fig.set_size_inches(18, 6, forward=True)

    # remove whitespace aroung figure before saving
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, 
                        wspace=0, hspace=0)

    # check if images directory exists
    im_dir_exists = os.path.exists('images')
    if not im_dir_exists:
        os.mkdir('images')
    im_dir_exists = os.path.exists('images/mathstats')
    if not im_dir_exists:
        os.mkdir('images/mathstats')

    # save
    fig.savefig('images/mathstats/'+fname, transparent=True, pad_inches=0, format=ftype, dpi=dpi)
