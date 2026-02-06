
import matplotlib.pyplot as plt
import numpy as np
import copy
import seaborn as sns
import math
import geopandas as gpd
import pandas as pd
import matplotlib.patches as mpatches
import contextily as cx
from shapely import geometry

from utils import *


class MapViser():
    def __init__(self) -> None:
        self.crs = 'epsg:4326'

        self.workdir = get_work_dir()

        self.load_base_geo()
        
        self.basemap_facecolor='gainsboro'
        
        self.basemap_edgecolor='white'
        
        self.vismap_edgecolor=None

        self.text_font = 'simhei'

        plt.rcParams['font.family'] = self.text_font
        
        #plt.rcParams['font.size'] = 16

        self.bound_color = 'lightgrey'


    def set_font(self,font="Arial"):
        self.text_font = font

        plt.rcParams['font.family'] = self.text_font

    
    def load_base_geo(self):
        self.wrld = gpd.read_file(self.workdir+'data/geo/Base/world_map.shp')
        self.land = gpd.read_file(self.workdir+'data/geo/Base/world_land.shp')
        
    
    def load_pa(self):
        self.pa = gpd.read_file(self.workdir+'data/geo/Base/world_pa.gpkg')
        

    def set_crs(self,crs=None):
        self.crs = crs


    def set_bound_color(self,color=None):
        self.bound_color = color


    def get_custom_bound(self,boundary):
        l = boundary[0]
        r = boundary[1]
        b = boundary[2]
        t = boundary[3]

        bound = gpd.GeoDataFrame({'id':[0,1]},
                                 geometry=[geometry.Point((l,b)),
                                           geometry.Point((r,t))],
                                 crs='epsg:4326')
        
        bound.to_crs(self.crs,inplace=True)

        return bound
        

    def add_colorbar(self,fig,
                          vmax,
                          label,
                          vmin=0,
                          extend='max',
                          orientation='vertical',
                          cmap='autumn_r',
                          loc=[0.175,0.35,0.02,0.225]):        

        cax = fig.add_axes(loc)
        
        im = plt.cm.ScalarMappable(cmap=cmap, 
                                   norm=plt.Normalize(vmin=vmin, vmax=vmax))
        
        cbar = fig.colorbar(im,
                            cax=cax,
                            extend=extend,
                            orientation=orientation)
        
        cbar.outline.set_edgecolor('none')
        
        cbar.ax.tick_params(labelsize=8) 
        
        for l in cbar.ax.yaxis.get_ticklabels():
            l.set_family('Arial')

        cax.yaxis.tick_left()
        
        cax.minorticks_on()
        
        cax.yaxis.set_tick_params(which='major', length=3)
        cax.yaxis.set_tick_params(which='minor', length=1.5)
        
        cbar_font = {'size':10}
        
        cbar.set_label(label,font=cbar_font)


    def draw_attr_map(self,vis_shp=None,
                           attr_col='capacity',
                           cmap=None,
                           out_fig=None,
                           markersize=None,
                           cbar_label=None,
                           bound_mode=0, #0,1,2
                           boundary=None,
                           attr_scale=1,
                           threshold=None,
                           add_basemap=0,
                           draw_pa=False,
                           with_legend=False,
                           lb=None,
                           ub=None,
                           lw=None,
                           with_cbar=True,
                           vis_wrld=True,
                           vis_grid=False,
                           return_fig=False):
        
        fig,ax = plt.subplots(figsize=(12.6,8.4),dpi=600)

        cmap = cmap if not cmap is None else 'plasma_r'
        
        if bound_mode == 0:
            ax.set_xlim(self.bound.geometry[0].x, 
                        self.bound.geometry[1].x)
            
            ax.set_ylim(self.bound.geometry[0].y, 
                        self.bound.geometry[1].y)
        elif bound_mode == 1 and not boundary is None:
            custom_bound = self.get_custom_bound(boundary=boundary)
            ax.set_xlim(custom_bound.geometry[0].x, 
                        custom_bound.geometry[1].x)
            
            ax.set_ylim(custom_bound.geometry[0].y, 
                        custom_bound.geometry[1].y)

        if vis_wrld:
            self.wrld.to_crs(self.crs).plot(ax=ax,
                                            facecolor=self.basemap_facecolor,
                                            edgecolor=self.basemap_edgecolor,
                                            linestyle='-',
                                            alpha=0.75,
                                            linewidth=0.45)

        self.land.boundary.to_crs(self.crs).plot(ax=ax,
                                                 edgecolor=self.bound_color,
                                                 linestyle='-',
                                                 linewidth=0.25)
        
        if add_basemap:
            cx.add_basemap(ax,crs=self.crs,attribution="")

        show_shp = copy.deepcopy(vis_shp)
        
        show_shp[attr_col] = show_shp[attr_col] * attr_scale

        vmin = np.min(show_shp[attr_col])
        vmax = np.max(show_shp[attr_col])

        if not threshold is None:
            show_shp = show_shp.loc[show_shp[attr_col]>threshold]

        if not lb is None:
            if np.min(show_shp[attr_col]) < lb:
                show_shp.loc[show_shp[attr_col]<lb,attr_col] = lb - 2e-2 * lb
                vmin = lb - 2e-2 * lb
            else:
                vmin = lb

        if not ub is None:
            if np.max(show_shp[attr_col]) > ub:
                show_shp.loc[show_shp[attr_col]>ub,attr_col] = ub + 2e-2 * ub
                vmax = ub + 2e-2 * ub
            else:
                vmax = ub


        show_shp.to_crs(self.crs).plot(ax=ax,
                                       column=attr_col,
                                       cmap=cmap,
                                       vmin=vmin,
                                       vmax=vmax,
                                       linewidth=lw,
                                       edgecolor=self.vismap_edgecolor,
                                       markersize=markersize)
        
        if draw_pa:
            self.pa.to_crs(self.crs).plot(ax=ax,
                                          facecolor='grey',
                                          hatch='//')
            
            ax.bar([],[],
                   facecolor='grey',
                   hatch='//',
                   label='Protected area')

        if with_cbar:
            self.add_colorbar(fig=fig,
                            vmax=vmax,
                            vmin=vmin,
                            label=cbar_label,
                            cmap=cmap,
                            loc=[0.175,0.39,0.02,0.2])
        ax.axis('off')
        
        ax.set_xticks([],[])
        ax.set_yticks([],[])

        '''ax.set_xticks(np.arange(-150,160,50),
                          [str(i)+'°' for i in np.arange(-150,160,50)],
                          font={'size':8})
        
        ax.set_yticks(np.arange(-60,90,20),
                          [str(i)+'°' for i in np.arange(-60,90,20)],
                          font={'size':8})'''
        
        if with_legend:
            ax.legend(loc='center left')

        if not return_fig:
            plt.savefig(out_fig,bbox_inches='tight')

            plt.close()
        else:
            return fig,ax