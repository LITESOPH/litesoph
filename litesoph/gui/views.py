from re import I
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog           # importing filedialog which is used for opening windows to read files.
from tkinter import messagebox
from  PIL import Image,ImageTk
from tkinter import font
# from numpy import matplotlib as plot

import pathlib

from litesoph.gui import images
from litesoph.simulations.filehandler import show_message
from litesoph.gui.input_validation import Onlydigits, Onechar, Decimalentry, Validatedconv, Fourchar
from litesoph.gui.widgets import LabelInput
from litesoph.gui.visual_parameter import myfont, myfont1, myfont2

class StartPage(tk.Frame):

    def __init__(self, parent, lsroot, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.lsroot = lsroot
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        

        mainframe = ttk.Frame(self,padding="12 12 24 24")
        #mainframe = ttk.Frame(self)
        mainframe.grid(column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        frame =ttk.Frame(self, relief=tk.SUNKEN, padding="6 6 0 24")
        #frame =ttk.Frame(self)
        frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        myFont = font.Font(family='Helvetica', size=15, weight='bold')
        j= font.Font(family ='Courier', size=20,weight='bold')
        k= font.Font(family ='Courier', size=40,weight='bold')
        l= font.Font(family ='Courier', size=10,weight='bold')
        
        gui_style = ttk.Style()
        gui_style.configure('TButton', foreground='black',background='gainsboro',font=('Helvetica', 20))

        #parent.configure(bg="grey60")

        # create a canvas to show project list icon
        canvas_for_project_list_icon=tk.Canvas(frame, bg='gray', height=400, width=400, borderwidth=0, highlightthickness=0)
        canvas_for_project_list_icon.grid(column=1, row=1, sticky=(tk.W, tk.E) ,columnspan=8,rowspan=8)
        #canvas_for_project_list_icon.place(x=5,y=5)

        #image_project_list = Image.open('images/project_list.png')
        #canvas_for_project_list_icon.image = ImageTk.PhotoImage(image_project_list.resize((100,100), Image.ANTIALIAS))
        #canvas_for_project_list_icon.create_image(0,0, image=canvas_for_project_list_icon.image, anchor='nw')
        
        #frame_1_label_1 = Label(frame,text="Manage Job(s)", fg="blue")
        #frame_1_label_1['font'] = myFont
        #frame_1_label_1.grid(row=10, column=2, sticky=(W, E) ,columnspan=3,rowspan=2)

        #label_1 = Label(mainframe,text="Welcome to LITESOPH", bg='#0052cc',fg='#ffffff')
        label_1 = tk.Label(mainframe,text="Welcome to LITESOPH",fg='blue')
        label_1['font'] = myFont
        #label_1.grid(row=0,column=1,sticky=(E,S))
        label_1.place(x=200,y=50)
        
        label_2 = tk.Label(mainframe,text="Layer Integrated Toolkit and Engine for Simulations of Photo-induced Phenomena",fg='blue')
        label_2['font'] = l
        label_2.grid(row=1,column=1)
        #label_2.place(x=200,y=100)

        # create a canvas to show image on
        canvas_for_image = tk.Canvas(mainframe, bg='gray', height=125, width=125, borderwidth=0, highlightthickness=0)
        #canvas_for_image.grid(row=30,column=0, sticky='nesw', padx=0, pady=0)
        canvas_for_image.place(x=30,y=5)

        image = Image.open(images.LITESOPH_LOGO_BIG)
        canvas_for_image.image = ImageTk.PhotoImage(image.resize((125, 125), Image.ANTIALIAS))
        canvas_for_image.create_image(0,0,image=canvas_for_image.image, anchor='nw')

        # create a canvas to show project list icon
        canvas_for_project_create=tk.Canvas(mainframe, bg='gray', height=50, width=50, borderwidth=0, highlightthickness=0)
        canvas_for_project_create.place(x=20,y=200)

        image_project_create = Image.open(images.PROJECT_CREATE_ICON)
        canvas_for_project_create.image = ImageTk.PhotoImage(image_project_create.resize((50,50), Image.ANTIALIAS))
        canvas_for_project_create.create_image(0,0, image=canvas_for_project_create.image, anchor='nw')

        button_create_project = tk.Button(mainframe,text="Start LITESOPH Project", activebackground="#78d6ff",command=lambda: self.event_generate('<<ShowWorkManagerPage>>'))
        button_create_project['font'] = myFont
        button_create_project.place(x=80,y=200)

        #button_open_project = Button(mainframe,text="About LITESOPH",fg="white")
        button_open_project = tk.Button(mainframe,text="About LITESOPH")
        button_open_project['font'] = myFont
        button_open_project.place(x=80,y=300)

class WorkManagerPage(tk.Frame):

    MainTask = ["Preprocessing Jobs","Simulations","Postprocessing Jobs"]
    Pre_task = ["Ground State","Geometry Optimisation"]
    Sim_task = ["Delta Kick","Gaussian Pulse"]
    Post_task = ["Spectrum","Dipole Moment and Laser Pulse","Kohn Sham Decomposition","Induced Density","Generalised Plasmonicity Index"]

    def __init__(self, parent, lsroot, directory, *args, **kwargs):
        super().__init__(parent,*args, **kwargs)
        
        self.lsroot = lsroot
        self.directory = directory
       
        self._default_var = {
            'proj_path' : ['str'],
            'proj_name' : ['str'],
            'task' : ['str', '--choose job task--'],
            'sub_task' : ['str']
        }
        self._var = var_define(self._default_var)
        
        myFont = font.Font(family='Helvetica', size=10, weight='bold')
        j= font.Font(family ='Courier', size=20,weight='bold')
        k= font.Font(family ='Courier', size=40,weight='bold')
        l= font.Font(family ='Courier', size=15,weight='bold')

        self.Frame1 =tk.Frame(self)
        self.Frame1.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), pady=10)
       
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(cursor="fleur")

        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_rowconfigure(2, weight=1)
        self.label_proj = tk.Label(self.Frame1,text="Project Name",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        self.label_proj.grid(column=0, row= 0, sticky=tk.W,  pady=10, padx=10)
        
        
        self.entry_proj = tk.Entry(self.Frame1,textvariable=self._var['proj_name'])
        self.entry_proj['font'] = myFont
        self.entry_proj.grid(column=1, row= 0, sticky=tk.W)
        self.entry_proj.delete(0, tk.END)
                
        self.button_project = tk.Button(self.Frame1,text="Create New Project",width=18, activebackground="#78d6ff",command=self._create_project)
        self.button_project['font'] = myFont
        self.button_project.grid(column=2, row= 0, sticky=tk.W, padx= 10, pady=10)
        
        
        self.button_project = tk.Button(self.Frame1,text="Open Existing Project",activebackground="#78d6ff",command=self._open_project)
        self.button_project['font'] = myFont
        self.button_project.grid(column=2, row= 2, sticky=tk.W, padx= 10, pady=10)

        self.Frame2 = tk.LabelFrame(self)
        self.Frame2.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.grid_columnconfigure(1, weight=1)


        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(cursor="fleur")

        self.Frame2_label_1 = tk.Label(self.Frame2, text="Upload Geometry",bg='gray',fg='black')  
        self.Frame2_label_1['font'] = myFont
        self.Frame2_label_1.grid(column=0, row= 0, sticky=tk.W,  pady=10, padx=10)
       

        self.Frame2_Button_1 = tk.Button(self.Frame2,text="Select",activebackground="#78d6ff",command=self._get_geometry_file)
        self.Frame2_Button_1['font'] = myFont
        self.Frame2_Button_1.grid(column=1, row= 0, sticky=tk.W,  pady=10, padx=10)
       

        self.message_label = tk.Label(self.Frame2, text='', foreground='red')
        self.message_label['font'] = myFont
        self.message_label.grid(column=2, row= 0, sticky=tk.W)
       
        
        self.Frame2_Button_1 = tk.Button(self.Frame2,text="View",activebackground="#78d6ff",command=self._geom_visual)
        self.Frame2_Button_1['font'] = myFont
        self.Frame2_Button_1.grid(column=3, row= 0, sticky=tk.W)
        

        self.label_proj = tk.Label(self.Frame2,text="Job Type",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        self.label_proj.grid(column=0, row= 1, sticky=tk.W,  pady=10, padx=10)
       
            
        self.entry_task = ttk.Combobox(self.Frame2,width= 30, textvariable= self._var['task'], values= self.MainTask)
        self.entry_task['font'] = myFont
        self.entry_task.grid(column=1, row= 1, columnspan=3, sticky=tk.W,  pady=10, padx=10)
       
        self.entry_task.bind("<<ComboboxSelected>>", self.pick_task)
        self.entry_task['state'] = 'readonly'

        self.Frame2_label_3 = tk.Label(self.Frame2, text="Sub Task",bg='gray',fg='black')
        self.Frame2_label_3['font'] = myFont
        self.Frame2_label_3.grid(column=0, row= 2, sticky=tk.W,  pady=10, padx=10)
        
          
        self.entry_sub_task = ttk.Combobox(self.Frame2, width= 30, textvariable=self._var['sub_task'], value = [''])
        self.entry_sub_task['font'] = myFont
        self.entry_sub_task.current(0)
        self.entry_sub_task.grid(column=1, row= 2, columnspan=3, sticky=tk.W,  pady=10, padx=10)       
        self.entry_sub_task['state'] = 'readonly'   

        # self.status_frame = tk.Frame(self)
        # self.status_frame.grid(row=3, column=0, sticky='nsew', columnspan=2)        
        # self.status_frame.configure(relief='groove',borderwidth="2",cursor="fleur")

        # update_label = tk.Label(self.status_frame)
        # update_label['font'] = myFont
        # update_label.grid(row=0, column=0)

        # self.text = View_Text(self.status_frame)
        # self.text.grid(row=0, column=0, sticky='nsew')
        # lines = "LITESOPH PROJECT"
        # self.text.text_view.insert('end', lines)
        # self.text.text_view.configure(state='disabled')
       
        self.Frame3 = tk.Frame(self )
        self.Frame3.grid(column=0, row=2, columnspan=1,  sticky=(tk.N, tk.W, tk.E, tk.S))        

        self.Frame3.configure(relief='groove')
        self.Frame3.configure(borderwidth="2")
        self.Frame3.configure(relief="groove")
        self.Frame3.configure(cursor="fleur")

        self.Frame3_Button_MainPage = tk.Button(self.Frame3, text="Start Page",activebackground="#78d6ff", command=lambda:self.event_generate('<<ShowStartPage>>'))
        self.Frame3_Button_MainPage['font'] = myFont
        self.Frame3_Button_MainPage.grid(column=0, row= 0, sticky="we")
           
        Frame3_Button1 = tk.Button(self.Frame3, text="Proceed",activebackground="#78d6ff",command=lambda:self.event_generate('<<SelectTask>>'))
        Frame3_Button1['font'] = myFont
        Frame3_Button1.grid(column=1, row= 0, sticky="we", padx=(600,0))
           

    def pick_task(self, *_):
            if self._var['task'].get() == "Preprocessing Jobs":
                self.entry_sub_task.config(value = self.Pre_task)
                self.entry_sub_task.current(0)
            if self._var['task'].get() == "Simulations":
                self.entry_sub_task.config(value = self.Sim_task)
                self.entry_sub_task.current(0)
            if self._var['task'].get() == "Postprocessing Jobs":
                self.entry_sub_task.config(value = self.Post_task)
                self.entry_sub_task.current(0)

    def update_project_entry(self, proj_path):
        proj_path = pathlib.Path(proj_path)
        self._var['proj_path'].set(proj_path.parent)
        self.entry_path.config(textvariable=self._var['proj_path'])
        self._var['proj_name'].set(proj_path.name)
        self.entry_proj.config(textvariable=self._var['proj_name'])

    def _open_project(self):
        self.event_generate('<<OpenExistingProject>>')

    def get_project_name(self):
        project_name = self.entry_proj.get()
        return project_name

    def _create_project(self):
        self.event_generate('<<CreateNewProject>>')

    def _get_geometry_file(self):
        self.event_generate('<<GetMolecule>>')
        show_message(self.message_label,"Uploaded")
    
    def _geom_visual(self):
        self.event_generate('<<VisualizeMolecule>>')
    
    def get_sub_task(self):
        return self._var['sub_task'].get()
        
    def refresh_var(self):
        for key, value in self._default_var.items():
            try:
                self._var[key].set(value[1])
            except IndexError:
                self._var[key].set('')    

def var_define(var_dict:dict):
    var_def_dict ={}
    for key, type_value in var_dict.items():
        type = type_value[0]
        try:
            value = type_value[1]
            if type == 'str':
                var ={ key : tk.StringVar(value=value)}
            elif type == 'int':
                var ={ key : tk.IntVar(value=value)}
            elif type == 'float':
                var ={ key : tk.DoubleVar(value=value)}
        except IndexError:
            if type == 'str':
                var ={ key : tk.StringVar()}
            elif type == 'int':
                var ={ key : tk.IntVar()}
            elif type == 'float':
                var ={ key : tk.DoubleVar()}   
         
        var_def_dict.update(var)

    return var_def_dict
        

class GeomOptPage(tk.Frame):

    Mainmode = ["gaussian"]
    nao_task = ["dzp","pvalence.dz"]
    fd_task = [""]
    pw_task = [""]
    gauss_task = ["6-31G","STO-2G","STO-3G","STO-6G","3-21G","3-21G*","6-31G*","6-31G**","6-311G","6-311G*","6-311G**","cc-pVDZ","aug-cc-pvtz"]
    octgp_box = ["parallelepiped","minimum", "sphere", "cylinder"]
    nw_box = ["None"]
    gp_box = ["parallelepiped"]
    xc_gp = ["LDA","PBE","PBE0","PBEsol","BLYP","B3LYP","CAMY-BLYP","CAMY-B3LYP"]
    xc_nw = ["acm","b3lyp","beckehandh","Hfexch","pbe0","becke88","xpbe96","bhlyp","cam-s12g","cam-s12h","xperdew91","pbeop"]
    xc_oct1 = ["lda_x_1d + lda_e_1d"]
    xc_oct2 = ["lda_x_2d + lda_c_2d_amgb"]
    xc_oct3 = ["lda_x + lda_c_pz_mod"]
    dxc_oct = ["1","2","3"]
    fnsmear = ["semiconducting","fermi_dirac","cold_smearing","methfessel_paxton","spline_smearing"]
    eignsolv = ["rmmdiis","plan","cg","cg_new"]

    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.controller = controller
        
        self.job = None
        
        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        j=font.Font(family ='Courier', size=20,weight='bold')
        k=font.Font(family ='Courier', size=40,weight='bold')
        l=font.Font(family ='Courier', size=15,weight='bold')
        
        self.optFrame1 = tk.Frame(self)
        self.optFrame1.configure(relief='groove')
        self.optFrame1.configure(borderwidth="2")
        self.optFrame1.configure(relief="groove")
        self.optFrame1.configure(cursor="fleur")
        self.optFrame1 = tk.Frame(self)
        
        self.mode = tk.StringVar()
        self.xc = tk.StringVar()
        self.basis = tk.StringVar()
        self.charge = tk.StringVar()
        self.maxiter = tk.IntVar()
        self.shape = tk.StringVar()
        self.spinpol = tk.StringVar()
        self.multip = tk.StringVar()
        self.h   = tk.StringVar()
        self.nbands = tk.StringVar()
        self.vacuum = tk.StringVar()
        self.energy = tk.DoubleVar()
        self.density = tk.DoubleVar()
        self.bands = tk.StringVar()
        self.theory = tk.StringVar()
        self.tolerances = tk.StringVar()
        self.dimension = tk.StringVar()
        self.lx = tk.DoubleVar()
        self.ly = tk.DoubleVar()
        self.lz = tk.DoubleVar()
        self.r = tk.DoubleVar()
        self.l = tk.DoubleVar()
        self.dxc = tk.StringVar()
        self.mix = tk.StringVar()
        self.eigen = tk.StringVar()
        self.smear = tk.StringVar()
        self.smearfn = tk.StringVar()
        self.unitconv = tk.StringVar()
        self.unit_box = tk.StringVar()
        self.operation = tk.StringVar()

        self.optFrame1.place(relx=0.01, rely=0.01, relheight=0.99, relwidth=0.492)
        self.optFrame1.configure(relief='groove')
        self.optFrame1.configure(borderwidth="2")
        self.optFrame1.configure(relief="groove")
        self.optFrame1.configure(cursor="fleur")            
        
        optlabel = tk.Label(self.optFrame1,text="LITESOPH input for Ground State",fg='blue')
        optlabel['font'] = myFont
        optlabel.place(x=150,y=10)
      
        optlabel = tk.Label(self.optFrame1,text="Mode",bg="gray",fg="black")
        optlabel['font'] = myFont
        optlabel.place(x=10,y=60)
        
        def pick_task(e):
            if task.get() == "nao":
                sub_task.config(value = self.nao_task)
                sub_task.current(0)
                box_shape.config(value = self.gp_box)
                box_shape.current(0)
                self.gpaw_frame()
            if task.get() == "fd":
                sub_task.config(value = self.fd_task)
                sub_task.current(0)
                box_shape.config(value = self.octgp_box)
                box_shape.set("--choose box--")
            if task.get() == "pw":
                sub_task.config(value = self.pw_task)
                sub_task.current(0)
                box_shape.config(value = self.gp_box)
                box_shape.current(0)
                self.gpaw_frame()
            if task.get() == "gaussian":
                sub_task.config(value = self.gauss_task)
                sub_task.current(0)
                box_shape.config(value = self.nw_box)
                box_shape.current(0)
                self.nwchem_optframe()
            

        task = ttk.Combobox(self.optFrame1, textvariable = self.mode, values= self.Mainmode)
        task.set("--choose mode--")
        task['font'] = myFont
        task.place(x=280,y=60)
        task.bind("<<ComboboxSelected>>", pick_task)
        task['state'] = 'readonly'

        basislabel = tk.Label(self.optFrame1, text="Basis",bg='gray',fg='black')
        basislabel['font'] = myFont
        basislabel.place(x=10,y=110)
          
        sub_task = ttk.Combobox(self.optFrame1, textvariable= self.basis, value = [" "])
        sub_task.current(0)
        sub_task['font'] = myFont
        sub_task.place(x=280,y=110)
        sub_task['state'] = 'readonly'

        chargelabel = tk.Label(self.optFrame1, text="Charge", bg= "grey",fg="black")
        chargelabel['font'] = myFont
        chargelabel.place(x=10,y=160)
    
        chargeentry = tk.Entry(self.optFrame1,textvariable= self.charge)
        chargeentry['font'] = myFont
        chargeentry.insert(0,"0")
        chargeentry.place(x=280,y=160)

        iterlabel = tk.Label(self.optFrame1, text="Maximum SCF iteration", bg= "grey",fg="black")
        iterlabel['font'] = myFont
        iterlabel.place(x=10,y=210)
 
        iterentry = tk.Entry(self.optFrame1,textvariable= self.maxiter)
        iterentry['font'] = myFont
        iterentry.delete(0,tk.END)
        iterentry.insert(0,"300")
        iterentry.place(x=280,y=210)

        enerlabel = tk.Label(self.optFrame1,text="Energy Convergence",bg="gray",fg="black")
        enerlabel['font'] = myFont
        enerlabel.place(x=10,y=260)

        enerentry_proj = tk.Entry(self.optFrame1, width= 10, textvariable= self.energy)
        enerentry_proj['font'] = myFont
        enerentry_proj.delete(0,tk.END)
        enerentry_proj.insert(0,"5.0e-7")
        enerentry_proj.place(x=280,y=260)
 
        optunit = ttk.Combobox(self.optFrame1,width=5, textvariable= self.unitconv , value = ["eV","au","Ha","Ry"])
        optunit.current(0)
        optunit['font'] = myFont
        optunit.place(x=380,y=260)
        optunit['state'] = 'readonly'
       
        boxlabel = tk.Label(self.optFrame1,text="Box Shape",bg="gray",fg="black")
        boxlabel['font'] = myFont
        boxlabel.place(x=10,y=310)
    
        def pick_frame(e):
            if box_shape.get() == "parallelepiped":
                if task.get() == "fd":
                    self.gp2oct()
            if box_shape.get() == "minimum": 
                self.oct_minsph_frame()
                self.octopus_frame()
            if box_shape.get() == "sphere":
                self.oct_minsph_frame()
                self.octopus_frame()
            if box_shape.get() == "cylinder": 
                self.oct_cyl_frame()
                self.octopus_frame()

        box_shape = ttk.Combobox(self.optFrame1, textvariable= self.shape, value = [" "])
        box_shape.current(0)
        box_shape['font'] = myFont
        box_shape.place(x=280,y=310)
        box_shape.bind("<<ComboboxSelected>>", pick_frame)
        box_shape['state'] = 'readonly'
       
        #self.Frame7 = tk.Frame(self)
        #self.Frame7.place(relx=0.1, rely=0.88, relheight=0.12, relwidth=0.492)

        #self.Frame7.configure(relief='groove')
        #self.Frame7.configure(borderwidth="2")
        #self.Frame7.configure(relief="groove")
        #self.Frame7.configure(cursor="fleur")
 
        optbutb = tk.Button(self.optFrame1, text="Back",activebackground="#78d6ff",command=lambda:[self.back_button()])
        optbutb['font'] = myFont
        optbutb.place(x=10,y=380)
      
        self.optFrame6 = tk.Frame(self)
        self.optFrame6.place(relx=0.5, rely=0.87, relheight=0.13, relwidth=0.492)

        self.optFrame6.configure(relief='groove')
        self.optFrame6.configure(borderwidth="2")
        self.optFrame6.configure(relief="groove")
        self.optFrame6.configure(cursor="fleur")

        optbutv = tk.Button(self.optFrame6, text="View Input", state= 'disabled',activebackground="#78d6ff",command=lambda:[self.view_button()])
        optbutv['font'] = myFont
        optbutv.place(x=10,y=10)

        optbuts = tk.Button(self.optFrame6, text="Save Input",activebackground="#78d6ff",command=lambda:[self.save_button()])
        optbuts['font'] = myFont
        optbuts.place(x=200,y=10)

        self.label_msg = tk.Label(self.optFrame6,text="")
        self.label_msg['font'] = myFont
        self.label_msg.place(x=300,y=12.5)

        optbutrj = tk.Button(self.optFrame6, text="Run Job", state='disabled', activebackground="#78d6ff",command=lambda:[self.run_job_button()])
        optbutrj['font'] = myFont
        optbutrj.place(x=380,y=10)
    
    def back_button(self):
        self.event_generate('<<ShowWorkManagerPage>>')

    def save_button(self):
        inp_dict = self.opt_inp2dict()
        self.init_task(inp_dict, 'opt')
        self.write_input()
        show_message(self.label_msg,"Saved")

    def view_button(self):
        inp_dict = self.opt_inp2dict()
        self.init_task(inp_dict, 'opt')
        self.controller._show_frame(TextViewerPage, GeomOptPage, None, task=self.controller.task)

    def run_job_button(self):
        try:
            getattr(self.job.engine,'directory')           
        except AttributeError:
            messagebox.showerror(message="Input not saved. Please save the input before job submission")
        else:
            self.event_generate('<<ShowJobSubmissionPage>>')

    def nwchem_optframe(self):   

        myFont = font.Font(family='Helvetica', size=10, weight='bold')
        j=font.Font(family ='Courier', size=20,weight='bold')
        k=font.Font(family ='Courier', size=40,weight='bold')
        l=font.Font(family ='Courier', size=15,weight='bold')
 
        self.optFrame2 = tk.Frame(self)
        self.optFrame2.place(relx=0.5, rely=0.01, relheight=0.87, relwidth=0.492)
        
        self.optFrame2.configure(relief='groove')
        self.optFrame2.configure(borderwidth="2")
        self.optFrame2.configure(relief="groove")
        self.optFrame2.configure(cursor="fleur")
        
        optxc = tk.Label(self.optFrame2,text="Exchange Corelation",bg="gray",fg="black")
        optxc['font'] = myFont
        optxc.place(x=10,y=60)

        optcomb = ttk.Combobox(self.optFrame2, textvariable= self.xc, value = self.xc_nw)
        optcomb.current(4)
        optcomb['font'] = myFont
        optcomb.place(x=280,y=60)
        optcomb['state'] = 'readonly'

        #self.label_proj = Label(self.Frame2,text="Theory",bg="gray",fg="black")
        #self.label_proj['font'] = myFont
        #self.label_proj.place(x=10,y=60)
        
        #self.entry_pol_x = ttk.Combobox(self.Frame2, textvariable= self.theory, value = ["scf","dft"])
        #self.entry_pol_x.current(1)
        #self.entry_pol_x['font'] = myFont
        #self.entry_pol_x.place(x=280,y=60)
        #self.entry_pol_x['state'] = 'readonly'

        optdclabel = tk.Label(self.optFrame2,text="Density Convergence",bg="gray",fg="black")
        optdclabel['font'] = myFont
        optdclabel.place(x=10,y=110)

        optdcentry = tk.Entry(self.optFrame2,textvariable= self.density)
        optdcentry['font'] = myFont
        optdcentry.delete(0,tk.END)
        optdcentry.insert(0,"1.0e-5")
        optdcentry.place(x=280,y=110)

        optmullabel = tk.Label(self.optFrame2,text="Multiplicity",bg="gray",fg="black")
        optmullabel['font'] = myFont
        optmullabel.place(x=10,y=160)

        optmulentry = tk.Entry(self.optFrame2,textvariable= self.multip)
        optmulentry['font'] = myFont
        optmulentry.delete(0,tk.END)
        optmulentry.insert(0,"1")
        optmulentry.place(x=280,y=160)

        opttolentry = tk.Label(self.optFrame2,text="Tolerance",bg="gray",fg="black")
        opttolentry['font'] = myFont
        opttolentry.place(x=10,y=210)

        opttolcomb = ttk.Combobox(self.optFrame2, textvariable= self.tolerances, value = ["tight","accCoul","radius"])
        opttolcomb.current(0)
        opttolcomb['font'] = myFont
        opttolcomb.place(x=280,y=210)
        opttolcomb['state'] = 'readonly'
        
        optopnlabel = tk.Label(self.optFrame2,text="Operation",bg="gray",fg="black")
        optopnlabel['font'] = myFont
        optopnlabel.place(x=10,y=210)

        optopncomb = ttk.Combobox(self.optFrame2, textvariable= self.operation, value = ["optimize","optimize+frequency"])
        optopncomb.current(0)
        optopncomb['font'] = myFont
        optopncomb.place(x=280,y=210)
        optopncomb['state'] = 'readonly'

    def opt_inp2dict(self):

        inp_dict_nwopt = {
            'mode': self.mode.get(),
            'xc': self.xc.get(),
            'tolerances': self.tolerances.get(),
            'basis': self.basis.get(),
            'energy': self.energy.get(),
            'density' : self.density.get(),
            'charge' : self.charge.get(),
            'multip' : self.multip.get(),
            'maxiter' : self.maxiter.get(),
            'properties':self.operation.get(),
            'engine':'nwchem'
                    }

        if self.mode.get() == "gaussian":
            inp_dict_nwopt['geometry'] = pathlib.Path(self.controller.directory) / "coordinate.xyz"
            return inp_dict_nwopt


class View_note(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.parent = parent
        self.job = None

        self.myFont = font.Font(family='Helvetica', size=10, weight='bold')

        notebook = ttk.Notebook(self)
        notebook.grid()
        
        self.Frame1 = tk.Frame(notebook, borderwidth=2, relief='groove')
        self.Frame2 = tk.Frame(notebook, borderwidth=2, relief='groove')
        self.Frame3 = tk.Frame(notebook, borderwidth=2, relief='groove')

        self.Frame1.grid(row=0, column=0)
        self.Frame2.grid(row=0, column=0)
        self.Frame3.grid(row=0, column=0)

        notebook.add(self.Frame1, text='General Info')
        notebook.add(self.Frame2, text='Advanced Info')
        notebook.add(self.Frame3, text='SCF Convergence')

        self.frame_button = tk.Frame(self, borderwidth=2, relief='groove')
        self.frame_button.grid(row=10, column=0,columnspan=10, sticky='nswe')
        # layout all of the main containers
        #self.grid_rowconfigure(0, weight=1)
        #self.grid_rowconfigure(0, weight=1)
        #self.grid_rowconfigure(1, weight=8)
        # self.grid_columnconfigure(9, weight=3)
        # self.grid_rowconfigure(1, weight=2)
        # self.grid_columnconfigure(5, weight=5)
        #self.grid_rowconfigure(2, weight=3)
        #self.grid_columnconfigure(8, weight=1)

        #self.Frame1.grid(row=1, rowspan=100, column=0,columnspan=4, sticky='nsew', ipadx=10, ipady=5)
        #self.Frame2.grid(row=1, column=5, columnspan=2, sticky='nsew')
        #self.Frame3.grid(row=1, column=9, sticky='nswe')
        #self.Frame2.grid(row=4,  sticky="nsew")
        # btm_frame.grid(row=3, sticky="ew")
        # btm_frame2.grid(row=4, sticky="ew")
        
        

    def add_jobsub(self):
        """ Adds Job Sub buttons to View_note"""

        self.frame_run = tk.Frame(self,borderwidth=2, relief='groove')
        self.frame_run.grid(row=0, column=1, sticky='nsew')

        self.Frame1_Button2 = tk.Button(self.frame_run, text="Submit Local", activebackground="#78d6ff", command=lambda: self.event_generate('<<SubLocalGroundState>>'))
        self.Frame1_Button2['font'] = myfont()
        self.Frame1_Button2.grid(row=1, column=2,padx=3, pady=3)
        
        self.Frame1_Button3 = tk.Button(self.frame_run, text="Submit Network", activebackground="#78d6ff", command=lambda: self.event_generate('<<SubNetworkGroundState>>'))
        self.Frame1_Button3['font'] = myfont()
        self.Frame1_Button3.grid(row=2, column=2, padx=3, pady=3)
        
          

class GroundStatePage(View_note):
  
    Mainmode = ["nao","fd","pw","gaussian"]
    nao_task = ["dzp","sz","dz","szp","pvalence.dz"]
    fd_task = [""]
    pw_task = [""]
    gauss_task = ["6-31G","STO-2G","STO-3G","STO-6G","3-21G","3-21G*","6-31G*","6-31G**","6-311G","6-311G*","6-311G**","cc-pVDZ","aug-cc-pvtz"]
    octgp_box = ["parallelepiped","minimum", "sphere", "cylinder"]
    nw_box = ["None"]
    gp_box = ["parallelepiped"]
    xc_gp = ["LDA","PBE","PBE0","PBEsol","BLYP","B3LYP","CAMY-BLYP","CAMY-B3LYP"]
    # xc_nw = ["acm","b3lyp","beckehandh","Hfexch","pbe0","becke88","xpbe96","bhlyp","cam-s12g","cam-s12h","xperdew91","pbeop"]
    xc_nw = ["pbe96","pbe0","b3lyp","pw91", "bp86", "bp91","bhlyp"]
    oct_lda_x = ["lda_x","lda_x_rel","lda_x_erf","lda_x_rae"]
    oct_lda_c = ["lda_c_pz_mod","lda_c_ob_pz","lda_c_pw","lda_c_ob_pw","lda_c_2d_amgb"]
    oct_pbe_x = ["gga_x_pbe","gga_x_pbe_r","gga_x_b86","gga_x_herman","gga_x_b86_mgc","gga_x_b88","gga_x_pbe_sol"]
    oct_pbe_c = ["gga_c_pbe","gga_c_tca","gga_c_lyp","gga_c_p86","gga_c_pbe_sol"]
    expt_option = ["yes", "no"]
    oct_expt_yes = ["pseudodojo_pbe","pseudodojo_pbe_stringent","pseudodojo_lda","pseudodojo_lda_stringent","pseudodojo_pbesol","pseudodojo_pbesol_stringent","sg15", "hscv_lda", "hscv_pbe"]
    oct_expt_no = ["standard", "hgh_lda_sc","hgh_lda"]
    fnsmear = ["semiconducting","fermi_dirac","cold_smearing","methfessel_paxton","spline_smearing"]
    eignsolv = ["rmmdiis","plan","cg","cg_new"]
    nwc_theory = ["SCF","DFT"]
    gpfnsmear = ["improved-tetrahedron-method","tetrahedron-method","fermi-dirac","marzari-vanderbilt"] 
    
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent,controller, *args, **kwargs)
        self.controller = controller
        
        self.job = None

        self._default_var = {
            'mode' : ['str', '--choose mode--'],
            'nwxc' : ['str', 'pbe0'],
            'gpxc' : ['str','LDA'],
            'var_oct_xc' : ['int', 1],
            'oct_xc' : ['str',''],
            'oct_x' : ['str',''],
            'oct_c' : ['str',''],
            'pseudo' : ['str', '--choose option--'],
            'expt' : ['str', '--choose option--'],
            'basis' : ['str', ''],
            'charge': ['int', 0],
            'maxiter' : ['int', 300],
            'shape' : ['str', ''],
            'gpspinpol' : ['str', 'None'],
            'ocspinpol' : ['str', 'unpolarized'],
            'multip' : ['int', 1],
            'h' : ['float', 0.3],
            'nbands' : ['str',''],
            'vacuum' : ['float', 6],
            'energy' : ['float', 5.0e-7],
            'density' : ['float', 1e-6],
            'bands' : ['str', 'occupied'],
            'tolerances' : ['str','tight'],
            'lx' : ['float',12],
            'ly' : ['float',12],
            'lz' : ['float',12],
            'r' : ['float',6],
            'l' : ['float',12],
            'dxc' : ['int', 3],
            'mix' : ['float', 0.3],
            'eigen' : ['str','rmmdiis'],
            'smear' : ['float', 0.1],
            'ocsmearfn' : ['str','semiconducting'],
            'gpsmearfn' : ['str','fermi-dirac'],
            'unitconv' : ['str'],
            'unit_box' : ['str','angstrom'],
            'theory' : ['str','DFT'],
            'gradient' : ['float', 1.0e-4],
            'eigenstate': ['float', 4e-8],
            'absdensity': ['float',0.0],
            'abseigen'  : ['float',0.0],
            'rlteigen'   : ['float',0.0]
        }
        self.add_jobsub()
        self._var = var_define(self._default_var)
        self.frame_collection()
        
        #self.test()
    
    # def add_jobsub(self):
    #     self.frame_run = tk.Frame(self)
    #     self.Frame1_sub = tk.Frame(self.Frame1, borderwidth=2, relief='groove')
    #     self.Frame1_sub.grid(row=0, column=0, rowspan=11, columnspan=10, sticky='we')
    #     self.Frame2_sub = tk.Frame(self.Frame2, borderwidth=2, relief='groove')
    #     self.Frame2_sub.grid(row=0, column=0, rowspan=11, columnspan=10, sticky= 'we') 
    #     self.Frame3_sub = tk.Frame(self.Frame3, borderwidth=2, relief='groove')
    #     self.Frame3_sub.grid(row=0, column=0, rowspan=11, columnspan= 10, sticky='we')

    def tab1_button_frame(self):

        myFont = font.Font(family='Helvetica', size=10, weight='bold')
        #btframe = tk.Frame(parent, borderwidth=2)
        #btframe.grid(row=101, column=0,columnspan=5, sticky='nswe')
        self.Frame1_Button1 = tk.Button(self.frame_button, text="Back", activebackground="#78d6ff", command=lambda: self.back_button())
        self.Frame1_Button1['font'] = myFont
        self.Frame1_Button1.grid(row=0, column=1, padx=3, pady=3,sticky='nsew')
        # self.frame_button.grid_columnconfigure(2, weight=1)
        # self.frame_button.grid_columnconfigure(4, weight=1)

    def tab2_button_frame(self):
        myFont = font.Font(family='Helvetica', size=10, weight='bold')
        #btframe = tk.Frame(parent, borderwidth=2)
        #btframe.grid(row=101, column=0,columnspan=5, sticky='nswe')
        self.Frame1_Button2 = tk.Button(self.frame_button, text="View Input", activebackground="#78d6ff", command=lambda: self.view_button())
        self.Frame1_Button2['font'] = myFont
        self.Frame1_Button2.grid(row=0, column=2,padx=3, pady=3,sticky='nsew')
        
        self.Frame1_Button3 = tk.Button(self.frame_button, text="Save Input", activebackground="#78d6ff", command=lambda: self.save_button())
        self.Frame1_Button3['font'] = myFont
        self.Frame1_Button3.grid(row=0, column=4, padx=3, pady=3,sticky='nsew')

        self.label_msg = tk.Label(self.frame_button,text="")
        self.label_msg['font'] = myFont
        self.label_msg.grid(row=0, column=3, sticky='nsew')

        # sub_job_option = ttk.Combobox(self.frame_button, textvariable = self._var['mode'], values= self.Mainmode)
        # sub_job_option['font'] = myFont
        # sub_job_option.grid(row=0, column= 6, sticky='we', padx=2, pady=2)
        # # sub_job_option.bind("<<ComboboxSelected>>", pick_job_option)
        # sub_job_option['state'] = 'readonly'
        # self.Frame1_Button3 = tk.Button(self.frame_button, text="Run Job", activebackground="#78d6ff", command=lambda: self.run_job_button())
        # self.Frame1_Button3['font'] = myFont
        # self.Frame1_Button3.grid(row=0, column=6, padx=3, pady=3)

    def mode_frame(self,parent):

        myFont = font.Font(family='Helvetica', size=10, weight='bold')
        mode_frame = tk.Frame(parent)
        mode_frame.grid(row=0, column=0)      

        self.heading = tk.Label(mode_frame,text="LITESOPH input for Ground State",fg='blue')
        self.heading['font'] = myFont
        self.heading.grid(row=0, column=0)
        
        
        self.label_proj = tk.Label(mode_frame,text="Mode",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        self.label_proj.grid(row=2, column=0, sticky='w', padx=2, pady=4)

        def pick_box(e):
            if task.get() == "nao":
                sub_task.config(value = self.nao_task)
                sub_task.current(0)
                self.box_shape.config(value = self.gp_box)
                self.box_shape.current(0)
                self.engine = 'gpaw'
                self.engine_specific_frame()
            if task.get() == "pw":
                sub_task.config(value = self.pw_task)
                sub_task.current(0)
                self.box_shape.config(value = self.gp_box)
                self.box_shape.current(0)
                self.engine = 'gpaw'
                self.engine_specific_frame()
            if task.get() == "gaussian":
                sub_task.config(value = self.gauss_task)
                sub_task.current(0)
                self.box_shape.config(value = self.nw_box)
                self.box_shape.current(0)
                self.engine = 'nwchem'
                self.engine_specific_frame()
            elif task.get() == "fd":
                sub_task.config(value = self.fd_task)
                sub_task.current(0)
                self.box_shape.config(value = self.octgp_box)
                self.box_shape.set("--choose box--")


        task = ttk.Combobox(mode_frame, textvariable = self._var['mode'], values= self.Mainmode)
        task['font'] = myFont
        task.grid(row=2, column= 1, sticky='w', padx=2, pady=2)
        task.bind("<<ComboboxSelected>>", pick_box)
        task['state'] = 'readonly'

        self.basis = tk.Label(mode_frame, text="Basis",bg='gray',fg='black')
        self.basis['font'] = myFont
        self.basis.grid(row=4, column=0, sticky='w', padx=2, pady=4)

        sub_task = ttk.Combobox(mode_frame, textvariable= self._var['basis'], value = [" "])
        sub_task['font'] = myFont
        sub_task.grid(row=4, column=1, sticky='w', padx=2, pady=2)
        sub_task['state'] = 'readonly'

        self.charge = tk.Label(mode_frame, text="Charge",  bg= "grey",fg="black")
        self.charge['font'] = myFont
        self.charge.grid(row=6, column=0, sticky='w', padx=2, pady=4)

        self.entry_chrg = Onlydigits(mode_frame,textvariable=self._var['charge'])
        self.entry_chrg['font'] = myFont
        self.entry_chrg.grid(row=6, column=1, sticky='w', padx=2, pady=2)


        self.shape = tk.Label(mode_frame,text="Box Shape",bg="gray",fg="black")
        self.shape['font'] = myFont
        self.shape.grid(row=8, column=0, sticky='w', padx=2, pady=4)

        def pick_frame(e):
            if self.box_shape.get() == "parallelepiped":
                if task.get() == "fd":
                    self.gp2oct()
            elif self.box_shape.get() in ["minimum","sphere","cylinder"] : 
                self.engine = 'octopus'
                self.engine_specific_frame()

        self.box_shape = ttk.Combobox(mode_frame, textvariable= self._var['shape'], value = [" "])
        self.box_shape.current(0)
        self.box_shape['font'] = myFont
        self.box_shape.bind("<<ComboboxSelected>>", pick_frame)
        self.box_shape['state'] = 'readonly'
        self.box_shape.grid(row=8, column=1, sticky='w', padx=2, pady=2)
       
        empty_frame = tk.Frame(mode_frame, borderwidth=2)
        empty_frame.grid(row=10, column=0)

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=2, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=4, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=6, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=8, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=10, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=12, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=14, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=16, column=0, sticky= 'NSEW')

        empty_frame.grid_columnconfigure(0, weight=1)
        empty_frame.grid_rowconfigure(1, weight=1)

             
    # def gp_simbox(self,parent):

    #     gp_simb = tk.Frame(parent)
    #     gp_simb.grid(row=1, column=0, sticky='w')
        
    #     myFont = font.Font(family='Helvetica', size=10, weight='bold')
 
    #     self.subheading = tk.Label(gp_simb,text="Simulation Box",fg='blue')
    #     self.subheading['font'] = myFont
    #     self.subheading.grid(row=0, column=0, sticky='w')
     
    #     self.label_sp = tk.Label(gp_simb,text="Spacing (in Ang)",bg="gray",fg="black")
    #     self.label_sp['font'] = myFont
    #     self.label_sp.grid(row=2, column=0, sticky='w', padx=2, pady=4)

    #     self.entry_sp = Decimalentry(gp_simb,textvariable= self._var['h'])  
    #     self.entry_sp['font'] = myFont
    #     self.entry_sp.grid(row=2, column=1, sticky='w', padx=8, pady=2)  
    
    #     self.Frame2_note = tk.Label(gp_simb,text="Vacuum size (in Ang)",bg="gray",fg="black")
    #     self.Frame2_note['font'] = myFont
    #     self.Frame2_note.grid(row=4, column=0, sticky='w', padx=2, pady=4)
       
    #     self.entry_vac = Decimalentry(gp_simb,textvariable= self._var['vacuum'])
    #     self.entry_vac['font'] = myFont
    #     self.entry_vac.grid(row=4, column=1, sticky='w', padx=8, pady=2)

    def oct_simbox(self, parent):
        self.oct_simb = tk.Frame(parent)
        self.oct_simb.grid(row=2, column=0, sticky='w')

        myFont = font.Font(family='Helvetica', size=10, weight='bold')
        j= font.Font(family ='Courier', size=20,weight='bold')
        k= font.Font(family ='Courier', size=40,weight='bold')
        l= font.Font(family ='Courier', size=15,weight='bold')

        self.subheading = tk.Label(self.oct_simb,text="Simulation Box",fg='blue')
        self.subheading['font'] = myFont
        self.subheading.grid(row=0, column=0, sticky='w')
  
        self.label_sp = tk.Label(self.oct_simb,text="Spacing (in Ang)",bg="gray",fg="black")
        self.label_sp['font'] = myFont
        self.label_sp.grid(row=2, column=0, sticky='w', padx=2, pady=4)

        self.entry_sp = Decimalentry(self.oct_simb,textvariable= self._var['h'])  
        self.entry_sp['font'] = myFont
        self.entry_sp.grid(row=2, column=1, sticky= 'w', padx=8, pady=2)

        self.boxlabel = tk.Label(self.oct_simb,text="Simulation box unit",bg="gray",fg="black")
        self.boxlabel['font'] = myFont
        self.boxlabel.grid(row=3, column=0, sticky='w', padx=2, pady=4)
        
        
        unit = ttk.Combobox(self.oct_simb, width=8, textvariable= self._var['unit_box'], value = ["angstrom","au"])
        unit.current(0)
        unit['font'] = myFont
        unit.grid(row=3, column=1, sticky='w', padx=12, pady=2)
        unit['state'] = 'readonly'

        # self.oct_minsph_frame(self.oct_simb)
        if self.box_shape.get() == "parallelepiped":
            self.oct_ppl_frame(self.oct_simb)
            # self.box1.grid(row=12, column=0, sticky='w', padx=2, pady=4)
                
        if self.box_shape.get() == "minimum": 
            self.oct_minsph_frame(self.oct_simb)
            # self.box1.grid(row=12, column=0, sticky='w', padx=2, pady=4)
                
        if self.box_shape.get() == "sphere":
            self.oct_minsph_frame(self.oct_simb)
            # self.box1.grid(row=12, column=0, sticky='w', padx=2, pady=4)
                
        if self.box_shape.get() == "cylinder": 
            self.oct_cyl_frame(self.oct_simb)
        # return oct_simb
  
    def oct_ppl_frame(self,parent):
    
        #ocp_frame = tk.Frame(self.Frame2, borderwidth=2)
        #ocp_frame.grid(row=0, column=0)

        #self.Frame3 = tk.Frame(self)
        #self.Frame3.place(relx=0.5, rely=0.01, relheight=0.2, relwidth=0.492)
      
        oct_ppd_frame = tk.Frame(parent)
        oct_ppd_frame.grid(row=4, column=0, columnspan=3)

        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        #self.Frame3.configure(relief='groove')
        #self.Frame3.configure(borderwidth="2")
        #self.Frame3.configure(relief="groove")
        #self.Frame3.configure(cursor="fleur")
   
        # self.boxlabel = tk.Label(oct_ppd_frame,text="Simulation box unit",bg="gray",fg="black")
        # self.boxlabel['font'] = myFont
        # #self.boxlabel.place(x=10,y=10)
        # self.boxlabel.grid(row=2, column=0, sticky='w', padx=2, pady=4)

        # unit = ttk.Combobox(oct_ppd_frame, width=5, textvariable= self._var['unit_box'], value = ["au","angstrom"])
        # unit.current(0)
        # unit['font'] = myFont
        # unit.grid(row=2, column=1, sticky='w', padx=8, pady=2)
        # unit['state'] = 'readonly'
       
        self.note = tk.Label(oct_ppd_frame,text="Length of Box (lx, ly, lz)",bg="gray",fg="black")
        self.note['font'] = myFont
        #self.note.place(x=10,y=40)
        self.note.grid(row=4, column=0, sticky='w', padx=2, pady=4)

        #self.entry1 = tk.Entry(self.Frame3,width= 5, textvariable= self._var['lx'])
        self.entry1 = Decimalentry(oct_ppd_frame, width =5, textvariable = self._var['lx'])
        self.entry1['font'] = myFont
        #self.entry1.place(x=220,y=40)
        self.entry1.grid(row=4, column=1, sticky='w', padx=8, pady=2)

        #self.entry2 = tk.Entry(self.Frame3, width= 5, textvariable= self._var['ly'])
        self.entry2 = Decimalentry(oct_ppd_frame,width= 5, textvariable= self._var['ly'])
        self.entry2['font'] = myFont
        #self.entry2.place(x=280,y=40)
        self.entry2.grid(row=4, column=2, sticky='w', padx=16, pady=2)

        #self.entry3 = tk.Entry(self.Frame3,width=5, textvariable= self._var['lz'])
        self.entry3 = Decimalentry(oct_ppd_frame, width= 5, textvariable= self._var['lz'])
        self.entry3['font'] = myFont
        #self.entry3.place(x=340,y=40)
        self.entry3.grid(row=4, column=3, sticky='w', padx=16, pady=2)
                  
    def oct_minsph_frame(self,parent):
  
        ocms_frame = tk.Frame(parent, borderwidth=2)
        ocms_frame.grid(row=4, column=0)

        #self.Frame3 = tk.Frame(self)
        #self.Frame3.place(relx=0.5, rely=0.01, relheight=0.2, relwidth=0.492)

        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        # self.boxlabel = tk.Label(ocms_frame,text="Simulation box unit",bg="gray",fg="black")
        # self.boxlabel['font'] = myFont
        # self.boxlabel.grid(row=2, column=0, sticky='w', padx=2, pady=4)
        
        
        # unit = ttk.Combobox(ocms_frame, width=5, textvariable= self._var['unit_box'], value = ["au","angstrom"])
        # unit.current(0)
        # unit['font'] = myFont
        # unit.grid(row=2, column=1, sticky='w', padx=12, pady=2)
        # unit['state'] = 'readonly'

        self.note = tk.Label(ocms_frame,text="Radius of Box",bg="gray",fg="black")
        self.note['font'] = myFont
        self.note.grid(row=4, column=0, sticky='w', padx=2, pady=4)

        #self.entryr = tk.Entry(self.Frame3, textvariable= self._var['r'], width= 7)
        self.entryr = Decimalentry(ocms_frame, textvariable= self._var['r'], width= 5)
        self.entryr['font'] = myFont
        self.entryr.grid(row=4, column=1, sticky='w', padx=12, pady=2)

    def oct_cyl_frame(self, parent):

        occyl_frame = tk.Frame(parent, borderwidth=2)
        occyl_frame.grid(row=4, column=0)

        #self.Frame3 = tk.Frame(self)
        #self.Frame3.place(relx=0.5, rely=0.01, relheight=0.2, relwidth=0.492)

        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        # self.boxlabel = tk.Label(occyl_frame,text="Simulation box unit",bg="gray",fg="black")
        # self.boxlabel['font'] = myFont
        # self.boxlabel.grid(row=2, column=0, sticky='w', padx=2, pady=4)

        # unit = ttk.Combobox(occyl_frame, width=9, textvariable= self._var['unit_box'], value = ["au","angstrom"])
        # unit.current(0)
        # unit['font'] = myFont
        # unit.grid(row=2, column=1, sticky='w', padx=12, pady=2)
        # unit['state'] = 'readonly'

        self.note1 = tk.Label(occyl_frame,text="Length of Cylinder",bg="gray",fg="black")
        self.note1['font'] = myFont
        self.note1.grid(row=4, column=0, sticky='w', padx=2, pady=4)

        #self.entryl = tk.Entry(self.Frame3, textvariable= self._var['l'], width= 5)
        self.entryl = Decimalentry(occyl_frame, textvariable= self._var['l'], width= 5)
        self.entryl['font'] = myFont
        self.entryl.grid(row=4, column=1, sticky='w', padx=12, pady=2)
 
        self.note2 = tk.Label(occyl_frame,text="Radius of Cylinder",bg="gray",fg="black")
        self.note2['font'] = myFont
        self.note2.grid(row=6, column=0, sticky='w', padx=2, pady=4)

        #self.entrycr = tk.Entry(self.Frame3, textvariable= self._var['r'], width= 5)
        self.entrycr = Decimalentry(occyl_frame, textvariable= self._var['r'], width= 5)
        self.entrycr['font'] = myFont
        self.entrycr.grid(row=6, column=1, sticky='w', padx=12, pady=2)
    
    def nwc_theory(self):
        nwc_thy = tk.Frame(self.Frame1_sub)
        nwc_thy.grid(row=8, column=0)
 
        myFont = font.Font(family='Helvetica', size=10, weight='bold')
      
        self.basis = tk.Label(nwc_thy, text="Theory",bg='gray',fg='black')
        self.basis['font'] = myFont
        #self.Frame2_label_3.place(x=10,y=110)
        self.basis.grid(row=2, column=0, sticky='w', padx=2, pady=4)

        sub_task = ttk.Combobox(nwc_thy, textvariable= self._var['theory'], value =["SCF","DFT"])
        sub_task['font'] = myFont
        #sub_task.place(x=280,y=110)
        sub_task.grid(row=2, column=1, ipadx=2, ipady=2)
        sub_task['state'] = 'readonly'
   
    
    def gp2oct(self):
        self.check = messagebox.askyesno(message= "The default engine for the input is gpaw, please click 'yes' to proceed with it. If no, octopus will be assigned")
        if self.check is True:
            self.engine = 'gpaw'
            self.engine_specific_frame()
        else:
            self.engine = 'octopus'
            self.engine_specific_frame()
 
    def back_button(self):
        self.event_generate('<<ShowWorkManagerPage>>')              
            
    def gpaw_frame(self,parent):  

        gp_frame = tk.Frame(parent, borderwidth=2)
        gp_frame.grid(row=0, column=0, sticky='w')
        #gp_frame.grid_columnconfigure(0, weight=1)

        #self.Frame2 = tk.Frame(self)
        #self.Frame2.place(relx=0.5, rely=0.01, relheight=0.87, relwidth=0.492)
        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        self.Frame2_note = tk.Label(gp_frame,text="LITESOPH input for Gpaw        ",fg="blue")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=0, column=0, sticky='w', padx=2, pady=4)

        self.Frame2_note = tk.Label(gp_frame,text="Exchange Correlation",bg="gray",fg="black")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=2, column=0, sticky='w', padx=2, pady=4)

        self.gpxc = ttk.Combobox(gp_frame, textvariable= self._var['gpxc'], value = self.xc_gp)
        self.gpxc.current(0)
        self.gpxc['font'] = myFont
        self.gpxc['state'] = 'readonly'
        self.gpxc.grid(row=2, column=1, sticky='w', padx=2, pady=2)

        self.spin = tk.Label(gp_frame,text="Spin Polarisation",bg="gray",fg="black")
        self.spin['font'] = myFont
        self.spin.grid(row=4, column=0, sticky='w', padx=2, pady=4)
   
        self.spinpol = ttk.Combobox(gp_frame, textvariable= self._var['gpspinpol'], value = ["None","True"])
        self.spinpol.current(0)
        self.spinpol['font'] = myFont
        self.spinpol['state'] = 'readonly'
        self.spinpol.grid(row=4, column=1, padx=2, pady=2)

        self.nb = tk.Label(gp_frame,text="Number of Bands",bg="gray",fg="black")
        self.nb['font'] = myFont
        self.nb.grid(row=6, column=0, sticky='w', padx=2, pady=4)

        self.entry_bands = Onlydigits(gp_frame,textvariable= self._var['nbands'])
        self.entry_bands['font'] = myFont
        self.entry_bands.grid(row=6, column=1, sticky='w', padx=2, pady=2)
      
        self.label_sp = tk.Label(gp_frame,text="Spacing (in Ang)",bg="gray",fg="black")
        self.label_sp['font'] = myFont
        self.label_sp.grid(row=8, column=0, sticky='w', padx=2, pady=4)

        self.entry_sp = Decimalentry(gp_frame,textvariable= self._var['h'])
        self.entry_sp['font'] = myFont
        self.entry_sp.grid(row=8, column=1, sticky='w', padx=2, pady=2)

        self.Frame2_note = tk.Label(gp_frame,text="Vacuum size (in Ang)",bg="gray",fg="black")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=10, column=0, sticky='w', padx=2, pady=4)

        self.entry_vac = Decimalentry(gp_frame,textvariable= self._var['vacuum'])
        self.entry_vac['font'] = myFont
        self.entry_vac.grid(row=10, column=1, sticky='w', padx=2, pady=2)
        

    def nwchem_frame(self,parent):   

        nw_frame = tk.Frame(parent, borderwidth=2)
        nw_frame.grid(row=0, column=0, sticky='w')
        #nw_frame.grid_columnconfigure(0, weight=1)
        #self.Frame2 = tk.Frame(self)
        #self.Frame2.place(relx=0.5, rely=0.01, relheight=0.87, relwidth=0.492)
        
        myFont = font.Font(family='Helvetica', size=10, weight='bold')
       
        self.Frame2_note = tk.Label(nw_frame,text="LITESOPH input for Nwchem      ",fg="blue")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=0, column=0, sticky='w', padx=2, pady=4)
 
        self.nwxc = tk.Label(nw_frame,text="Exchange Correlation",bg="gray",fg="black")
        self.nwxc['font'] = myFont
        self.nwxc.grid(row=2, column=0, sticky='w', padx=2, pady=4)

        self.entry_pol_x = ttk.Combobox(nw_frame, textvariable= self._var['nwxc'], value = self.xc_nw)
        self.entry_pol_x.current(4)
        self.entry_pol_x['font'] = myFont
        self.entry_pol_x['state'] = 'readonly'
        self.entry_pol_x.grid(row=2, column=1, sticky='w', padx=2, pady=2)
   
        self.mul = tk.Label(nw_frame,text="Multiplicity",bg="gray",fg="black")
        self.mul['font'] = myFont
        #self.mul.place(x=10,y=160)
        self.mul.grid(row=4, column=0, sticky='w', padx=2, pady=4)

        #self.entry_mul = tk.Entry(self.Frame2,textvariable= self._var['multip'])
        self.entry_mul = Onlydigits(nw_frame,textvariable= self._var['multip'])
        self.entry_mul['font'] = myFont
        #self.entry_mul.insert(0,"1")
        #self.entry_mul.place(x=280,y=160)
        self.entry_mul.grid(row=4, column=1, sticky='w', padx=2, pady=2)
      
        self.Frame2_note = tk.Label(nw_frame,text="Tolerances",bg="gray",fg="black")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=6, column=0, sticky='w', padx=2, pady=4)

        self.entry_pol_x = ttk.Combobox(nw_frame, textvariable= self._var['tolerances'], value = ["tight","accCoul","radius"])
        self.entry_pol_x.current(0)
        self.entry_pol_x['font'] = myFont
        self.entry_pol_x.grid(row=6, column=1, sticky='w', padx=2, pady=2)
        self.entry_pol_x['state'] = 'readonly'
 
        em_frame = tk.Frame(nw_frame, borderwidth=2)
        em_frame.grid(row=8, column=0)
        
        title = tk.Label(em_frame,  height=3)
        title.grid(row=0, column=0, sticky= 'NSEW')

        em_frame.grid_columnconfigure(0, weight=1)
        em_frame.grid_rowconfigure(1, weight=1)
 
    def octopus_frame(self,parent): 
        """Creates widgets for advanced info tab/Octopus""" 

        oct_frame = tk.Frame(parent, borderwidth=2)
        oct_frame.grid(row=1, column=0, sticky='nsew')
        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        self.Frame2_note = tk.Label(oct_frame,text="LITESOPH input for Octopus     ",fg="blue")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=0, column=0, sticky='w', padx=2, pady=6)
         
        self.expt_label = tk.Label(oct_frame,text="Experimental Features",bg="gray",fg="black")
        self.expt_label['font'] = myFont
        self.expt_label.grid(row=2, column=0, sticky='w', padx=2, pady=6)

        def pick_expt(e):
            if self.expt_combo.get() == "yes":
                self.cb1.config(value = self.oct_expt_yes)
                self.cb1.current(0)
                self.cb1.set("--choose option")
            if self.expt_combo.get() == "no":
                self.cb1.config(value = self.oct_expt_no)
                self.cb1.current(0)
                self.cb1.set("--choose option")

        self.expt_combo = ttk.Combobox(oct_frame,width= 10, textvariable= self._var['expt'], value = self.expt_option)
        self.expt_combo['font'] = myFont
        self.expt_combo.bind("<<ComboboxSelected>>", pick_expt)
        self.expt_combo['state'] = 'readonly'
        self.expt_combo.grid(row=2, column=1, sticky='we', padx=2, pady=6)

        self.lb1 = tk.Label(oct_frame,text="Pseudo Potential",bg="gray",fg="black")
        self.lb1['font'] = myFont
        self.lb1.grid(row=3, column=0, sticky='w', padx=2, pady=6)

        def pick_xc(e):
            if self._var['expt'].get() == "no":
                self.x_entry.config(value = self.oct_lda_x)
                self.x_entry.current(0)
                self.c_entry.config(value = self.oct_lda_c)
                self.c_entry.current(0)

            elif self._var['expt'].get() == "yes":
                pbe_list = ["pseudodojo_pbe","pseudodojo_pbe_stringent","pseudodojo_pbesol","pseudodojo_pbesol_stringent","sg15","hscv_pbe"]
                lda_list = ["pseudodojo_lda","hscv_lda"]
                #oct_expt_yes = ["pseudodojo_pbe","pseudodojo_pbe_stringent","pseudodojo_lda","pseudodojo_lda_stringent","pseudodojo_pbesol","pseudodojo_pbesol_stringent","sg15", "hscv_lda", "hscv_pbe"]
                if self._var['pseudo'].get() in pbe_list:
                    self.x_entry.config(value = self.oct_pbe_x)
                    self.x_entry.current(0)
                    self.c_entry.config(value = self.oct_pbe_c)
                    self.c_entry.current(0)
                elif self._var['pseudo'].get() in lda_list:
                    self.x_entry.config(value = self.oct_lda_x)
                    self.x_entry.current(0)
                    self.c_entry.config(value = self.oct_lda_c)
                    self.c_entry.current(0)

        self.cb1 = ttk.Combobox(oct_frame,width= 10, textvariable= self._var['pseudo'], value = "-- choose option --")
        self.cb1['font'] = myFont
        self.cb1.bind("<<ComboboxSelected>>", pick_xc)
        self.cb1['state'] = 'readonly'
        self.cb1.grid(row=3, column=1, sticky='we', padx=2, pady=6)

        oct_xc_frame = tk.Frame(oct_frame)
        oct_xc_frame.grid(row = 5, column=0, columnspan=4)
       
        self.Frame2_note = tk.Label(oct_frame,text="Exchange Correlation",bg="gray",fg="black")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=4, column=0, sticky='w', padx=4, pady=6)
        
        x_label = tk.Label(oct_xc_frame,text="x",bg="gray",fg="black")
        x_label['font'] = myFont
        x_label.grid(row=0, column=1, sticky='we', padx=2, pady=4)

        self.x_entry = ttk.Combobox(oct_xc_frame, textvariable= self._var['oct_x'])
        self.x_entry['font'] = myFont
        self.x_entry.grid(row=0, column=2, sticky='we', padx=2, pady=4)
        self.x_entry['state'] = 'readonly'

        c_label = tk.Label(oct_xc_frame,text="c",bg="gray",fg="black")
        c_label['font'] = myFont
        c_label.grid(row=0, column=3, sticky='we', padx=2, pady=4)

        self.c_entry = ttk.Combobox(oct_xc_frame, textvariable= self._var['oct_c'])
        self.c_entry['font'] = myFont
        self.c_entry.grid(row=0, column=4, sticky='we', padx=2, pady=4)
        self.c_entry['state'] = 'readonly'  

        def frame_destroy(frame:tk.Frame):
            for widget in frame.winfo_children():
                print(widget)
                widget.destroy()  

        self.Frame2_note = tk.Label(oct_frame,text="Spin Polarisation",bg="gray",fg="black")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=6, column=0, sticky='w', padx=2, pady=6)

        self.entry_pol_x = ttk.Combobox(oct_frame, textvariable= self._var['ocspinpol'], value = ["unpolarized","spin_polarized", "spinors"])
        self.entry_pol_x.current(0)
        self.entry_pol_x['font'] = myFont
        self.entry_pol_x['state'] = 'readonly'
        self.entry_pol_x.grid(row=6, column=1, sticky='w', padx=2, pady=6)
    
        self.Frame2_note = tk.Label(oct_frame,text="Eigen Solver",bg="gray",fg="black")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=8, column=0, sticky='w', padx=2, pady=6)

        self.entry_pol_x = ttk.Combobox(oct_frame, textvariable= self._var['eigen'], value = self.eignsolv)
        self.entry_pol_x.current(0)
        self.entry_pol_x['font'] = myFont
        self.entry_pol_x['state'] = 'readonly'
        self.entry_pol_x.grid(row=8, column=1, sticky='w', padx=2, pady=6)              
    
    def nwchem_convergence(self, parent):
        #parent.grid_remove()
        nwchem_conv = tk.Frame(parent, borderwidth=2)
        nwchem_conv.grid(row=0, column=0, sticky='w')

        myFont = font.Font(family='Helvetica', size=10, weight='bold')
     
        self.label_pol_z = tk.Label(nwchem_conv, text="SCF Convergence for NWChem     ", fg="blue")
        self.label_pol_z['font'] = myFont
        self.label_pol_z.grid(row=0, column=0, sticky='w', padx=2, pady=4)

        self.label_pol_z = tk.Label(nwchem_conv, text="Maximum SCF iteration", bg= "grey",fg="black")
        self.label_pol_z['font'] = myFont
        self.label_pol_z.grid(row=2, column=0, sticky='w', padx=2, pady=4)

        #entry = ttk.Entry(self.Frame1,textvariable= self._var['maxiter'])
        entry = Onlydigits(nwchem_conv,textvariable= self._var['maxiter'])
        entry['font'] = myFont
        entry.grid(row=2, column=1, sticky='w', padx=6, pady=2)

        self.Frame2_note = tk.Label(nwchem_conv,text="Energy(in au)",bg="gray",fg="black")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=4, column=0, sticky='w', padx=2, pady=4)

        self.entry_ener = tk.Entry(nwchem_conv, textvariable= self._var['energy'])
        #self.entry_ener = Validatedconv(self.Frame1)
        self.entry_ener['font'] = myFont
        self.entry_ener.grid(row=4, column=1, sticky='w', padx=2, pady=2)

        self.label_proj = tk.Label(nwchem_conv,text="Density",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=10,y=10)
        self.label_proj.grid(row=6, column=0, sticky='w', padx=2, pady=4)

        self.entry_proj = tk.Entry(nwchem_conv,textvariable= self._var['density'])
        self.entry_proj['font'] = myFont
        self.entry_proj.delete(0,tk.END)
        self.entry_proj.insert(0,"1.0e-4")
        #self.entry_proj.place(x=280,y=10)
        self.entry_proj.grid(row=6, column=1, sticky='w', padx=2, pady=2)

        self.label_proj = tk.Label(nwchem_conv,text="Gradient",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=10,y=10)
        self.label_proj.grid(row=8, column=0, sticky='w', padx=2, pady=4)

        self.entry_grd = tk.Entry(nwchem_conv,textvariable= self._var['gradient'])
        self.entry_grd['font'] = myFont
        self.entry_grd.delete(0,tk.END)
        self.entry_grd.insert(0,"1.0e-4")
        #self.entry_proj.place(x=280,y=10)
        self.entry_grd.grid(row=8, column=1, sticky='w', padx=2, pady=2)
   
        empty_frame = tk.Frame(nwchem_conv, borderwidth=2)
        empty_frame.grid(row=10, column=0)

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=2, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=4, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=6, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=8, column=0, sticky= 'NSEW')
      
        title = tk.Label(empty_frame,  height=3)
        title.grid(row=10, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=12, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=14, column=0, sticky= 'NSEW')
 
        title = tk.Label(empty_frame,  height=3)
        title.grid(row=16, column=0, sticky= 'NSEW')

        empty_frame.grid_columnconfigure(0, weight=1)
        empty_frame.grid_rowconfigure(1, weight=1)

    def gpaw_convergence(self, parent):
        # parent.grid_remove()
        gp_conv = tk.Frame(parent, borderwidth=2)
        gp_conv.grid(row=0, column=0, sticky='w')

        myFont = font.Font(family='Helvetica', size=10, weight='bold')
        
        self.label_pol_z = tk.Label(gp_conv, text="SCF Convergence for Gpaw       ", fg="blue")
        self.label_pol_z['font'] = myFont
        self.label_pol_z.grid(row=0, column=0, sticky='w', padx=2, pady=4)
 
        self.label_pol_z = tk.Label(gp_conv, text="Maximum SCF iteration", bg= "grey",fg="black")
        self.label_pol_z['font'] = myFont
        self.label_pol_z.grid(row=2, column=0, sticky='w', padx=2, pady=4)

        #entry = ttk.Entry(self.Frame1,textvariable= self._var['maxiter'])
        entry = Onlydigits(gp_conv,textvariable= self._var['maxiter'])
        entry['font'] = myFont
        entry.grid(row=2, column=1, sticky='w', padx=2, pady=2)

        self.Frame2_note = tk.Label(gp_conv,text="Energy(in au)",bg="gray",fg="black")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=4, column=0, sticky='w', padx=2, pady=4)

        self.entry_ener = tk.Entry(gp_conv, textvariable= self._var['energy'])
        #self.entry_ener = Validatedconv(self.Frame1)
        self.entry_ener['font'] = myFont
        self.entry_ener.grid(row=4, column=1, sticky='w', padx=2, pady=2)

        self.label_proj = tk.Label(gp_conv,text="Density",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=10,y=10)
        self.label_proj.grid(row=6, column=0, sticky='w', padx=2, pady=4)

        self.entry_proj = tk.Entry(gp_conv,textvariable= self._var['density'])
        self.entry_proj['font'] = myFont
        self.entry_proj.delete(0,tk.END)
        self.entry_proj.insert(0,"1.0e-4")
        #self.entry_proj.place(x=280,y=10)
        self.entry_proj.grid(row=6, column=1, sticky='w', padx=2, pady=2)

        self.label_proj = tk.Label(gp_conv,text="eigenstates",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=10,y=10)
        self.label_proj.grid(row=8, column=0, sticky='w', padx=2, pady=4)

        self.entry_proj = tk.Entry(gp_conv,textvariable= self._var['eigenstate'])
        self.entry_proj['font'] = myFont
        self.entry_proj.delete(0,tk.END)
        self.entry_proj.insert(0,"1.0e-4")
        #self.entry_proj.pl]ace(x=280,y=10)
        self.entry_proj.grid(row=8, column=1, sticky='w', padx=2, pady=2)
    
        self.bdocc = tk.Label(gp_conv,text="Band Occupancy",bg="gray",fg="black")
        self.bdocc['font'] = myFont
        #self.bdocc.place(x=10,y=310)
        self.bdocc.grid(row=10, column=0, sticky='w', padx=2, pady=4)

        self.occ = ttk.Combobox(gp_conv, textvariable= self._var['bands'], value = ["occupied","unoccupied"])
        self.occ.current(0)
        self.occ['font'] = myFont
        #self.occ.place(x=280,y=310)
        self.occ['state'] = 'readonly'
        self.occ.grid(row=10, column=1, sticky='w', padx=2, pady=2)

        self.lb2 = tk.Label(gp_conv,text="Smearing Function",bg="gray",fg="black")
        self.lb2['font'] = myFont
        #self.lb2.place(x=10,y=110)
        self.lb2.grid(row=12, column=0, sticky='w', padx=2, pady=4)

        self.entry_pol_x = ttk.Combobox(gp_conv, textvariable= self._var['gpsmearfn'], value = self.gpfnsmear)
        self.entry_pol_x.current(0)
        self.entry_pol_x['font'] = myFont
        #self.entry_pol_x.place(x=280,y=110)
        self.entry_pol_x['state'] = 'readonly'
        self.entry_pol_x.grid(row=12, column=1, sticky='w', padx=2, pady=2)

        self.label_proj = tk.Label(gp_conv, text="Smearing (eV)",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=260,y=60)
        self.label_proj.grid(row=14, column=0, sticky='w', padx=2, pady=4)

        #self.entry_proj = tk.Entry(self.Frame2, width= 7,textvariable= self._var['smear'])
        self.entry_sm = Decimalentry(gp_conv, width= 7, textvariable= self._var['smear']) 
        self.entry_sm['font'] = myFont
        #self.entry_sm.place(x=360,y=60)
        self.entry_sm.grid(row=14, column=1, sticky='w', padx=2, pady=2)
 
        empty_frame = tk.Frame(gp_conv, borderwidth=2)
        empty_frame.grid(row=16, column=0, sticky='w')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=2, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=4, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=6, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=8, column=0, sticky= 'NSEW')

        title = tk.Label(empty_frame,  height=3)
        title.grid(row=10, column=0, sticky= 'NSEW')

        empty_frame.grid_columnconfigure(0, weight=1)
        empty_frame.grid_rowconfigure(1, weight=1)

    def octopus_convergence(self, parent):
        oct_conv = tk.Frame(parent, borderwidth=2)
        oct_conv.grid(row=0, column=0, sticky = 'w')
        
        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        self.label_pol_z = tk.Label(oct_conv, text="SCF Convergence for Octopus    ", fg="blue")
        self.label_pol_z['font'] = myFont
        self.label_pol_z.grid(row=0, column=0, sticky='w', padx=2, pady=4)
      
        self.label_pol_z = tk.Label(oct_conv, text="Maximum SCF iteration", bg= "grey",fg="black")
        self.label_pol_z['font'] = myFont
        self.label_pol_z.grid(row=2, column=0, sticky='w', padx=2, pady=4)

        #entry = ttk.Entry(self.Frame1,textvariable= self._var['maxiter'])
        entry = Onlydigits(oct_conv,textvariable= self._var['maxiter'])
        entry['font'] = myFont
        entry.grid(row=2, column=1, sticky='w', padx=2, pady=2)

        self.Frame2_note = tk.Label(oct_conv,text="Energy(in au)",bg="gray",fg="black")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=4, column=0, sticky='w', padx=2, pady=4)

        self.entry_ener = tk.Entry(oct_conv, textvariable= self._var['energy'])
        #self.entry_ener = Validatedconv(self.Frame1)
        self.entry_ener['font'] = myFont
        self.entry_ener.grid(row=4, column=1, sticky='w', padx=2, pady=2)

        self.label_proj = tk.Label(oct_conv,text="Density",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=10,y=10)
        self.label_proj.grid(row=6, column=0, sticky='w', padx=2, pady=4)

        self.entry_proj = tk.Entry(oct_conv,textvariable= self._var['density'])
        self.entry_proj['font'] = myFont
        self.entry_proj.delete(0,tk.END)
        self.entry_proj.insert(0,"1.0e-4")
        #self.entry_proj.place(x=280,y=10)
        self.entry_proj.grid(row=6, column=1, sticky='w', padx=2, pady=2)
 
        self.label_proj = tk.Label(oct_conv,text="Absolute Convergence",fg="blue")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=10,y=10)
        self.label_proj.grid(row=8, column=0, sticky='w', padx=2, pady=4)

        self.label_proj = tk.Label(oct_conv,text="Density",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=10,y=10)
        self.label_proj.grid(row=10, column=0, sticky='w', padx=2, pady=4)

        self.entry_proj = tk.Entry(oct_conv,textvariable= self._var['absdensity'])
        self.entry_proj['font'] = myFont
        self.entry_proj.delete(0,tk.END)
        self.entry_proj.insert(0,"0.0")
        #self.entry_proj.place(x=280,y=10)
        self.entry_proj.grid(row=10, column=1, sticky='w', padx=2, pady=2)
     
        self.label_proj = tk.Label(oct_conv,text="Sum of eigen values",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=10,y=10)
        self.label_proj.grid(row=12, column=0, sticky='w', padx=2, pady=4)

        self.entry_proj = tk.Entry(oct_conv,textvariable= self._var['abseigen'])
        self.entry_proj['font'] = myFont
        self.entry_proj.delete(0,tk.END)
        self.entry_proj.insert(0,"0.0")
        #self.entry_proj.place(x=280,y=10)
        self.entry_proj.grid(row=12, column=1, sticky='w', padx=2, pady=2)
    
        #oct_rlt = tk.Frame(parent, borderwidth=2)
        #oct_rlt.grid(row=1, column=0)

        #myFont = font.Font(family='Helvetica', size=10, weight='bold')
 
        self.label_proj = tk.Label(oct_conv,text="Relative Convergence",fg="blue")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=10,y=10)
        self.label_proj.grid(row=14, column=0, sticky='w', padx=2, pady=4)
        
        self.label_proj = tk.Label(oct_conv, text="Sum of eigen values",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=10,y=10)
        self.label_proj.grid(row=16, column=0, sticky='w', padx=2, pady=4)

        self.entry_proj = tk.Entry(oct_conv, textvariable= self._var['rlteigen'])
        self.entry_proj['font'] = myFont
        self.entry_proj.delete(0,tk.END)
        self.entry_proj.insert(0,"0.0")
        #self.entry_proj.place(x=280,y=10)
        self.entry_proj.grid(row=16, column=1, sticky='w', padx=2, pady=2)

        #oct_mix = tk.Frame(parent, borderwidth=2)
        #oct_mix.grid(row=2, column=0)

        #myFont = font.Font(family='Helvetica', size=10, weight='bold')

        self.lb = tk.Label(oct_conv,text="Other Scf Parameters",fg="blue")
        self.lb['font'] = myFont
        #self.lb2.place(x=260,y=10)
        self.lb.grid(row=18, column=0, sticky='w', padx=2, pady=4)

        self.lb2 = tk.Label(oct_conv,text="Mixing",bg="gray",fg="black")
        self.lb2['font'] = myFont
        #self.lb2.place(x=260,y=10)
        self.lb2.grid(row=20, column=0, sticky='w', padx=2, pady=4)

        #self.en1 = tk.Entry(self.Frame2,width= 7, textvariable= self._var['mix'])
        self.en1 = Decimalentry(oct_conv, textvariable= self._var['mix'])
        self.en1['font'] = myFont
        #self.en1.place(x=360,y=10)
        self.en1.grid(row=20, column=1, sticky='w',padx=2, pady=2)

        self.label_proj = tk.Label(oct_conv, text="Smearing (eV)",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        #self.label_proj.place(x=260,y=60)
        self.label_proj.grid(row=22, column=0, sticky='w', padx=2, pady=4)

        #self.entry_proj = tk.Entry(self.Frame2, width= 7,textvariable= self._var['smear'])
        self.entry_sm = Decimalentry(oct_conv, textvariable= self._var['smear']) 
        self.entry_sm['font'] = myFont
        #self.entry_sm.place(x=360,y=60)
        self.entry_sm.grid(row=22, column=1, sticky='w', padx=2, pady=2)

        self.lb2 = tk.Label(oct_conv,text="Smearing Function",bg="gray",fg="black")
        self.lb2['font'] = myFont
        #self.lb2.place(x=10,y=110)
        self.lb2.grid(row=24, column=0, sticky='w', padx=2, pady=4)

        self.entry_pol_x = ttk.Combobox(oct_conv, textvariable= self._var['ocsmearfn'], value = self.fnsmear)
        self.entry_pol_x.current(0)
        self.entry_pol_x['font'] = myFont
        #self.entry_pol_x.place(x=280,y=110)
        self.entry_pol_x['state'] = 'readonly'
        self.entry_pol_x.grid(row=24, column=1, sticky='w', padx=2, pady=2)

    def frame_collection(self):
        self.Frame1_sub = tk.Frame(self.Frame1, borderwidth=2)
        self.Frame1_sub.grid(row=0, column=0, rowspan=11, columnspan=10, sticky='we')
        self.Frame2_sub = tk.Frame(self.Frame2, borderwidth=2)
        self.Frame2_sub.grid(row=0, column=0, rowspan=11, columnspan=10, sticky= 'we') 
        self.Frame3_sub = tk.Frame(self.Frame3, borderwidth=2)
        self.Frame3_sub.grid(row=0, column=0, rowspan=11, columnspan= 10, sticky='we')
        self.mode_frame(self.Frame1_sub)
        self.tab1_button_frame()
        self.tab2_button_frame()
        #self.common_convergence(self.Frame3)

    def engine_specific_frame(self):
        # self.Frame2_sub = tk.Frame(self.Frame2, borderwidth=2, relief='groove')
        # self.Frame2_sub.grid(row=0, column=0, rowspan=11, columnspan=10, sticky= 'we') 
        # self.Frame3_sub = tk.Frame(self.Frame3, borderwidth=2, relief='groove')
        # self.Frame3_sub.grid(row=0, column=0, rowspan=11, columnspan= 10, sticky='we')
        if self.engine == "nwchem":
            #To refresh the frames by removing the all existing widgets 

            for widget in self.Frame2_sub.winfo_children():
                widget.destroy()
            for widget in self.Frame3_sub.winfo_children():
                widget.destroy()

            self.nwchem_frame(self.Frame2_sub)
            self.nwchem_convergence(self.Frame3_sub)

        if self.engine == "gpaw":
            for widget in self.Frame2_sub.winfo_children():
                widget.destroy()
            for widget in self.Frame3_sub.winfo_children():
                widget.destroy()

            self.gpaw_frame(self.Frame2_sub)
            self.gpaw_convergence(self.Frame3_sub)  

        if self.engine == "octopus":
            for widget in self.Frame2_sub.winfo_children():
                widget.destroy()
            for widget in self.Frame3_sub.winfo_children():
                widget.destroy()
            
            self.octopus_frame(self.Frame2_sub)
            self.oct_simbox(self.Frame2_sub)               
            self.octopus_convergence(self.Frame3_sub)

        # if self.box_shape.get() == "minimum":
        #     self.oct_simbox(self.Frame1)
        #     self.oct_minsph_frame(self.oct_simbox)
        #     self.octopus_frame(self.Frame2)               
        #     self.octopus_convergence(self.Frame3)
        # if self.box_shape.get() == "sphere":
        #     self.oct_simbox(self.Frame1)
        #     self.oct_minsph_frame(self.oct_simbox)
        #     self.octopus_frame(self.Frame2)
        #     self.octopus_convergence(self.Frame3)
        # if self.box_shape.get() == "parallelepiped":
        #     if self.task.get() == "fd":
        #         self.gp2oct()

        
        #self.gpaw_convergence(self.Frame3)

    def min_parameters(self):
        
        from litesoph.utilities.units import au_to_eV
        inp_dict_gp = {
            'mode': self._var['mode'].get(),
            'xc': self._var['gpxc'].get(),
            'vacuum': self._var['vacuum'].get(),
            'basis':{'default': self._var['basis'].get()},
            'h': self._var['h'].get(),
            'nbands' : self._var['nbands'].get(),
            'charge' : self._var['charge'].get(),
            'spinpol' : self._var['gpspinpol'].get(), 
            'multip' : self._var['multip'].get(), 
            'maxiter' : self._var['maxiter'].get(),
            'box': self._var['shape'].get(),
            'properties': 'get_potential_energy()',
            'engine':'gpaw',
            #'geometry': str(self.controller.directory)+"/coordinate.xyz"
                    }   

        inp_dict_nw = {
            'mode': self._var['mode'].get(),
            'xc': self._var['nwxc'].get(),
            'tolerances': self._var['tolerances'].get(),
            'basis': self._var['basis'].get(),
            'energy': self._var['energy'].get(),
            'density' : self._var['density'].get(),
            'charge' : self._var['charge'].get(),
            'gradient':self._var['gradient'].get(),
            'multip' : self._var['multip'].get(),
            'maxiter' : self._var['maxiter'].get(),
            'engine':'nwchem',
            #'geometry': str(self.controller.directory)+"/coordinate.xyz"
                    }

        inp_dict_oct = {
            'mode': self._var['mode'].get(),
            'xc': self._var['ocxc'].get(),
            'energy': self._var['energy'].get(),
            'dimension' : self._var['dxc'].get(),
            'spacing': self._var['h'].get(),
            'spin_pol': self._var['ocspinpol'].get(),
            'charge': self._var['charge'].get(),
            'e_conv': self._var['energy'].get(),
            'max_iter': self._var['maxiter'].get(),
            'eigensolver':self._var['eigen'].get(),
            'smearing':self._var['smear'].get(),
            'smearing_func':self._var['ocsmearfn'].get(),
            'mixing':self._var['mix'].get(),
            'box':{'shape':self._var['shape'].get()},
            'unit_box' : self._var['unit_box'].get(),
            'engine':'octopus',
            #'geometry': str(self.controller.directory)+"/coordinate.xyz"
                    }      

        if self.engine == "nwchem":
           
            return inp_dict_nw

    def get_parameters(self):
        
        from litesoph.utilities.units import au_to_eV
        inp_dict_gp = {
            'mode': self._var['mode'].get(),
            'xc': self._var['gpxc'].get(),
            'vacuum': self._var['vacuum'].get(),
            'basis':{'default': self._var['basis'].get()},
            'h': self._var['h'].get(),
            'nbands' : self._var['nbands'].get(),
            'charge' : self._var['charge'].get(),
            'spinpol' : self._var['gpspinpol'].get(), 
            'multip' : self._var['multip'].get(), 
            'convergence': {'energy' : self._var['energy'].get() * round(au_to_eV,2),  # eV / electron f'{x: .2e}'
                        'density' :  self._var['density'].get(),
                        'eigenstates': self._var['eigenstate'].get(),  # eV^2
                        'bands' : self._var['bands'].get()}, 
            'maxiter' : self._var['maxiter'].get(),
            'box': self._var['shape'].get(),
            'properties': 'get_potential_energy()',
            'engine':'gpaw',
            #'geometry': str(self.controller.directory)+"/coordinate.xyz"
                    }   

        inp_dict_nw = {
            'mode': self._var['mode'].get(),
            'xc': self._var['nwxc'].get(),
            'tolerances': self._var['tolerances'].get(),
            'basis': self._var['basis'].get(),
            'energy': self._var['energy'].get(),
            'density' : self._var['density'].get(),
            'charge' : self._var['charge'].get(),
            'gradient':self._var['gradient'].get(),
            'multip' : self._var['multip'].get(),
            'maxiter' : self._var['maxiter'].get(),
            'engine':'nwchem',
            #'geometry': str(self.controller.directory)+"/coordinate.xyz"
                    }

        inp_dict_oct = {
            'mode': self._var['mode'].get(),
            'exp' : self._var['expt'].get(),
            'xc': {'option':1,'x':self._var['oct_x'].get(),'c':self._var['oct_c'].get()},
            'pseudo' : self._var['pseudo'].get(),
            'energy': self._var['energy'].get(),
            'dimension' : self._var['dxc'].get(),
            'spacing': self._var['h'].get(),
            'spin_pol': self._var['ocspinpol'].get(),
            'charge': self._var['charge'].get(),
            'e_conv': self._var['energy'].get(),
            'max_iter': self._var['maxiter'].get(),
            'eigensolver':self._var['eigen'].get(),
            'smearing':self._var['smear'].get(),
            'smearing_func':self._var['ocsmearfn'].get(),
            'mixing':self._var['mix'].get(),
            'box':{'shape':self._var['shape'].get()},
            'unit_box' : self._var['unit_box'].get(),
            'engine':'octopus',
            #'geometry': str(self.controller.directory)+"/coordinate.xyz"
                    }      

        if self.engine == "nwchem":
           
            return inp_dict_nw

        elif self.engine == 'gpaw':
            if self._var['basis'].get() == '':
                inp_dict_gp['basis']={}

            if self._var['mode'].get() == 'nao':
                inp_dict_gp['mode']='lcao'

            if self._var['nbands'].get() == '':
                inp_dict_gp['nbands']= None
           
            return inp_dict_gp

        elif self.engine == 'octopus':
            if self._var['shape'].get() in ['minimum','sphere']:
                inp_dict_oct['box']={'shape':self._var['shape'].get(),'radius':self._var['r'].get()}
            if self._var['shape'].get() == 'cylinder':
                inp_dict_oct['box']={'shape':self._var['shape'].get(),'radius':self._var['r'].get(),'xlength':self._var['l'].get()}
            if self._var['shape'].get() == 'parallelepiped':
                inp_dict_oct['box']={'shape':self._var['shape'].get(),'sizex':self._var['lx'].get(), 'sizey':self._var['ly'].get(), 'sizez':self._var['lz'].get()}
            
            return inp_dict_oct
       
    def set_label_msg(self,msg):
        show_message(self.label_msg, msg)
            
    def save_button(self):
        self.event_generate('<<SaveGroundStateScript>>')          

    def view_button(self):
        self.event_generate('<<ViewGroundStateScript>>')

    def run_job_button(self):
        self.event_generate('<<SubGroundState>>')

    def refresh_var(self):
        for key, value in self._default_var.items():
            try:
                self._var[key].set(value[1])
            except IndexError:
                self._var[key].set('')     

    def read_atoms(self, geom_xyz):
        from ase.io import read
        atoms = read(geom_xyz)
        atom_list = list(atoms.symbols)
        return atom_list

class View1(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.controller = controller
        self.parent = parent
        self.job = None

        self.myFont = font.Font(family='Helvetica', size=10, weight='bold')

        self.Frame1 = tk.Frame(self, borderwidth=2, relief='groove')
        self.Frame2 = tk.Frame(self, borderwidth=2, relief='groove')
        #self.Frame3 = tk.Frame(self, borderwidth=2, relief='groove')
        self.frame_button = tk.Frame(self, borderwidth=2, relief='groove')
        # layout all of the main containers
        #self.grid_rowconfigure(0, weight=1)
        #self.grid_rowconfigure(0, weight=1)
        #self.grid_rowconfigure(1, weight=8)
        self.grid_columnconfigure(9, weight=3)
        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(5, weight=5)
        #self.grid_rowconfigure(2, weight=3)
        #self.grid_columnconfigure(8, weight=1)

        self.Frame1.grid(row=1,column=0, columnspan=4, rowspan=100, sticky='nsew')
        self.Frame2.grid(row=1, column=5, rowspan=100,columnspan=2, sticky='nsew')
        #self.Frame3.grid(row=1, column=9, sticky='nswe')
        #self.Frame2.grid(row=4,  sticky="nsew")
        # btm_frame.grid(row=3, sticky="ew")
        # btm_frame2.grid(row=4, sticky="ew")
        
        self.frame_button.grid(row=101, column=0,columnspan=5, sticky='nswe')

    def add_job_frame(self, task_name):  
        """  Adds submit job buttons to View1"""

        self.Frame3 = tk.Frame(self, borderwidth=2, relief='groove')
        self.Frame3.grid(row=1, column=9, sticky='nswe')
        # View_Button1 = tk.Button(self.Frame3, text="View Output", activebackground="#78d6ff", command=lambda: [self.view_button()])
        # View_Button1['font'] = self.myFont
        # View_Button1.grid(row=2, column=1, sticky='nsew')

        self.Frame1_Button2 = tk.Button(self.Frame3, text="Submit Local", activebackground="#78d6ff", command=lambda: self.event_generate('<<SubLocal'+task_name+'>>'))
        self.Frame1_Button2['font'] = myfont()
        self.Frame1_Button2.grid(row=1, column=2,padx=3, pady=3)
        
        self.Frame1_Button3 = tk.Button(self.Frame3, text="Submit Network", activebackground="#78d6ff", command=lambda: self.event_generate('<<SubNetwork'+task_name+'>>'))
        self.Frame1_Button3['font'] = myfont()
        self.Frame1_Button3.grid(row=2, column=2, padx=3, pady=3)



class TimeDependentPage(View1):

    def __init__(self, parent, controller, engine, *args, **kwargs):
        super().__init__(parent,*args, **kwargs)
        self.parent = parent
        self.controller = controller
        
        self.engine = engine
        self.job = None

        myFont = font.Font(family='Helvetica', size=10, weight='bold')
          
        self._default_var = {
            'strength': ['float', 1e-5],
            'ex': ['int', 0],
            'ey': ['int', 0],
            'ez': ['int', 0],
            'dt': ['float'],
            'Nt': ['int'],
            'var1': ['int', 1],
            'var2': ['int',0]
        }
        self.gpaw_td_default = {
            'dt': ['float', 10],
            'Nt': ['int', 2000]
        }
        self.oct_td_default = {
            'dt': ['float', 2.4],
            'Nt': ['int', 1500]
        }
        self.nwchem_td_default = {
            'dt': ['float', 2.4],
            'Nt': ['int', 2000]
        }
        self._var = var_define(self._default_var)

        self.grid_columnconfigure(9, weight=3)
        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(5, weight=5)

        # self.add_job_frame() 

        self.Frame1_label_path = tk.Label(
            self, text="LITESOPH input for Delta Kick", fg='blue')
        self.Frame1_label_path['font'] = myFont
        self.Frame1_label_path.grid(row=0, column=3)
        # self.Frame1_label_path.place(x=150,y=10)

        self.label_proj = tk.Label(
            self.Frame1, text="Laser strength in a.u", bg="gray", fg="black", justify='left')
        self.label_proj['font'] = myFont
        self.label_proj.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        # self.label_proj.place(x=10,y=60)

        inval = ["1e-5", "1e-4", "1e-3"]
        self.entry_inv = ttk.Combobox(
            self.Frame1, textvariable=self._var['strength'], value=inval)
        self.entry_inv['font'] = myFont
        # self.entry_inv.place(x=280,y=60)
        self.entry_inv.grid(row=2, column=1)
        self.entry_inv['state'] = 'readonly'

        self.label_proj = tk.Label(
            self.Frame1, text="Propagation time step (in attosecond)", bg="gray", fg="black")
        self.label_proj['font'] = myFont
        self.label_proj.grid(row=3, column=0, sticky='w', padx=2, pady=4)

        #self.entry_proj = tk.Entry(self.Frame1,textvariable= self._var['dt'])
        self.entry_dt = Decimalentry(self.Frame1, textvariable=self._var['dt'])
        self.entry_dt['font'] = myFont
        self.entry_dt.grid(row=3, column=1, ipadx=2, ipady=2)

        self.label_proj = tk.Label(
            self.Frame1, text="Total time steps", bg="gray", fg="black")
        self.label_proj['font'] = myFont
        self.label_proj.grid(row=4, column=0, sticky='w', padx=2, pady=4)

        #self.entry_proj = tk.Entry(self.Frame1,textvariable= self._var['Nt'])
        self.entry_nt = Onlydigits(self.Frame1, textvariable=self._var['Nt'])
        self.entry_nt['font'] = myFont
        self.entry_nt.grid(row=4, column=1, ipadx=2, ipady=2)

        self.label_select = tk.Label(
            self.Frame1, text="Please select preferred option:", bg="gray", fg="black")
        self.label_select['font'] = myFont
        self.label_select.grid(row=5, column=0, sticky='w', padx=2, pady=4)

        values = {"Averaged spectrum": 1, "Specific polarization direction": 2}
        for (text, value) in values.items():
            tk.Radiobutton(self.Frame1, text=text, variable=self._var['var1'], font=myFont, justify='left',
                           value=value).grid(row=value+5, column=0, ipady=5, sticky='w')

        frame_pol = tk.Frame(self.Frame1, borderwidth=2)
        frame_pol.grid(row=8, column=0)
        
        # label_add = tk.Label(frame_pol, text="Please add polarization vectors:", bg="gray", fg="black")
        # label_add['font'] = myFont
        # label_add.grid(row=0, column=1, sticky='w', padx=2, pady=4)
        
        label_E = tk.Label(frame_pol, text="E:",  fg="black", font=myFont)
        label_E.grid(row=1, column =0, sticky='nsew')

        pol_list = [0, 1]
        self.entry_pol_x = ttk.Combobox(frame_pol, textvariable=self._var['ex'], value=pol_list, width=3)
        self.entry_pol_x['font'] = myFont
        self.entry_pol_x.grid(row=1, column=1, padx=2, pady=2)
        self.entry_pol_x['state'] = 'readonly'

        self.entry_pol_y = ttk.Combobox(frame_pol, textvariable=self._var['ey'], value=pol_list, width=3)
        self.entry_pol_y['font'] = myFont
        self.entry_pol_y.grid(row=1, column=2, padx=2, pady=2)
        self.entry_pol_y['state'] = 'readonly'

        self.entry_pol_z = ttk.Combobox(
            frame_pol, textvariable=self._var['ez'], value=pol_list, width=3)
        self.entry_pol_z['font'] = myFont
        self.entry_pol_z.grid(row=1, column=3, padx=2, pady=2)
        self.entry_pol_z['state'] = 'readonly'

        # Frame1_Button3 = tk.Button(frame_pol, text="Add",activebackground="#78d6ff",command=lambda:self.add_button())
        # Frame1_Button3['font'] = myFont
        # Frame1_Button3.grid(row =1, column=4, padx =5, pady=2)

        # options = [1,2,3,4]
        # options.append([self._var['ex'].get(),self._var['ez'].get()])
        # E_list = tk.Listbox(frame_pol)
        # E_list.grid(row=2, column=1)
        # for i in range(len(options)):
        #     E_list.insert(i,options[i])

        self.Frame1_Button1 = tk.Button(self.frame_button, text="Back", activebackground="#78d6ff", command=lambda: self.back_button())
        self.Frame1_Button1['font'] = myFont
        self.Frame1_Button1.grid(row=0, column=1, sticky='nsew', padx=3, pady=3)
        self.frame_button.grid_columnconfigure(2, weight=1)
        self.frame_button.grid_columnconfigure(4, weight=1)
        self.Frame1_Button2 = tk.Button(self.frame_button, text="View Input", activebackground="#78d6ff", command=lambda: self.view_button())
        self.Frame1_Button2['font'] = myFont
        self.Frame1_Button2.grid(row=0, column=3, sticky='nsew', padx=3, pady=3)
        
        self.Frame1_Button3 = tk.Button(self.frame_button, text="Save Input", activebackground="#78d6ff", command=lambda: self.save_button())
        self.Frame1_Button3['font'] = myFont
        self.Frame1_Button3.grid(row=0, column=5, sticky='nswe', padx=3, pady=3)

        self.label_msg = tk.Label(self.frame_button,text="")
        self.label_msg['font'] = myFont
        self.label_msg.grid(row=0, column=4)

        self.Frame2_note = tk.Label(self.Frame2, text="Note: Please select wavefunction \n for Kohn Sham Decomposition", fg="black")
        self.Frame2_note['font'] = myFont
        self.Frame2_note.grid(row=2, column=6)

        values = {"Wavefunction": 2}
        # Loop is used to create multiple Radiobuttons
        # rather than creating each button separately
        for (text, value) in values.items():
            tk.Checkbutton(self.Frame2, text=text, variable=self._var['var2'], font=myFont, onvalue=1, offvalue=0).grid(row=value+3, column=6, ipady=5, sticky='w')

    def pol_option(self):
        if self._var['var1'] == 1:
            pass
        elif self._var['var1'] == 2:
            pass    

    def get_parameters(self):
        kick = [float(self._var['strength'].get())*float(self._var['ex'].get()),
                float(self._var['strength'].get())*float(self._var['ey'].get()),
                float(self._var['strength'].get())*float(self._var['ez'].get())]
        inp_list = [float(self._var['dt'].get()),int(self._var['Nt'].get())]

        td_dict_gp = {
            'absorption_kick':kick,
            'analysis_tools':self.analysis_tool(),
            'propagate': tuple(inp_list)
        }

        td_dict_oct = {
            'max_step' : self._var['Nt'].get() ,
            'time_step' : self._var['dt'].get(),
            'td_propagator' : 'aetrs',
            'strength': self._var['strength'].get(),
            'e_pol': [self._var['ex'].get(),self._var['ey'].get(),self._var['ez'].get()]
          }

        td_dict_nwchem = {

            'tmax': self._var['Nt'].get() * self._var['dt'].get(),
            'dt': self._var['dt'].get(),
            'max':self._var['strength'].get(),
            'e_pol': [self._var['ex'].get(),self._var['ey'].get(),self._var['ez'].get()]

            }

        if self.engine == 'gpaw':
            return td_dict_gp
        elif self.engine == 'nwchem':
            return td_dict_nwchem
        elif self.engine == 'octopus':
            return td_dict_oct

    def analysis_tool(self):
        if self._var['var2'].get() == 1:
            return("wavefunction")

    def set_label_msg(self,msg):
        show_message(self.label_msg, msg)

    def save_button(self):
        self.event_generate('<<SaveRT_TDDFT_DELTAScript>>')

    def view_button(self):
        self.event_generate('<<ViewRT_TDDFT_DELTAScript>>')

    def run_job_button(self):
        self.event_generate('<<SubRT_TDDFT_DELTA>>')

    def back_button(self):
        self.event_generate('<<ShowWorkManagerPage>>')

    def update_var(self, default_dict:dict):
        for key, value in default_dict.items():
            try:
                self._var[key].set(value[1])
            except IndexError:
                self._var[key].set('')

    def update_engine_default(self, engn):
        self.engine = engn
        if engn == 'gpaw':
            self.update_var(self.gpaw_td_default)
        elif engn == 'octopus':
            self.update_var(self.oct_td_default)
        elif engn == 'nwchem':
            self.update_var(self.nwchem_td_default)


class LaserDesignPage(tk.Frame):

    def __init__(self, parent, controller, engine, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.engine = engine
        
        self.job = None
        self.tdpulse_dict = {}
        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        j=font.Font(family ='Courier', size=20,weight='bold')
        k=font.Font(family ='Courier', size=40,weight='bold')
        l=font.Font(family ='Courier', size=15,weight='bold')
        
        self.Frame1 = tk.Frame(self)
        #self.Frame1.place(relx=0.01, rely=0.01, relheight=0.99, relwidth=0.489)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(cursor="fleur")
        self.Frame1 = tk.Frame(self)
        
        self.strength = tk.DoubleVar()
        self.inval = tk.DoubleVar()
        self.pol_x = tk.StringVar()
        self.pol_y =  tk.StringVar()
        self.pol_z =  tk.StringVar()
        self.fwhm = tk.DoubleVar()
        self.frequency =  tk.DoubleVar()
        self.ts =  tk.DoubleVar()
        self.ns =  tk.IntVar()
        self.tin =  tk.DoubleVar()

        self.Frame1.place(relx=0.01, rely=0.01, relheight=0.99, relwidth=0.492)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(cursor="fleur")
        
        self.Frame1_label_path = tk.Label(self.Frame1,text="LITESOPH Input for Laser Design", fg='blue')
        self.Frame1_label_path['font'] = myFont
        self.Frame1_label_path.place(x=125,y=10)

        self.label_proj = tk.Label(self.Frame1,text="Time Origin (tin)",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        self.label_proj.place(x=10,y=60)

        #self.entry_proj = tk.Entry(self.Frame1,textvariable= self.tin)
        self.entry_tin = Decimalentry(self.Frame1, textvariable= self.tin)
        self.entry_tin['font'] = myFont
        self.tin.set(0)
        self.entry_tin.place(x=280,y=60)
        
        self.label_inval = tk.Label(self.Frame1,text="-log((E at tin)/Eo),(value>=6)",bg="gray",fg="black")
        self.label_inval['font'] = myFont
        self.label_inval.place(x=10,y=100)
 
        # inval_list = ["1e-8", "1e-9"]
        # self.entry_pol_z = ttk.Combobox(self.Frame1,textvariable= self.inval, value = inval_list)
        # self.entry_pol_z['font'] = myFont
        # self.entry_pol_z.insert(0,"1e-8")
        #self.entry_inval = tk.Entry(self.Frame1,textvariable= self.inval)
        self.entry_inval = Onlydigits(self.Frame1, textvariable= self.inval)
        self.entry_inval['font'] = myFont
        self.inval.set(6)
        self.entry_inval.place(x=280,y=100)

        self.label_proj = tk.Label(self.Frame1,text="Laser Strength in a.u (Eo)",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        self.label_proj.place(x=10,y=140)
    
        instr = ["1e-5","1e-4","1e-3"]
        self.entry_proj = ttk.Combobox(self.Frame1,textvariable= self.strength, value = instr)
        self.entry_proj['font'] = myFont
        self.entry_proj.current(0)
        self.entry_proj.place(x=280,y=140)
        self.entry_proj['state'] = 'readonly'

        self.label_proj = tk.Label(self.Frame1,text="Full Width Half Max (FWHM in eV)",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        self.label_proj.place(x=10,y=180)

        #self.entry_fwhm = tk.Entry(self.Frame1,textvariable= self.fwhm)
        self.entry_fwhm = Decimalentry(self.Frame1, textvariable= self.fwhm)
        #self.fwhm.set("0.2")
        self.entry_fwhm['font'] = myFont
        self.entry_fwhm.place(x=280,y=180)

        self.label_proj = tk.Label(self.Frame1,text="Frequency in eV",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        self.label_proj.place(x=10,y=220)

        #self.entry_proj = tk.Entry(self.Frame1,textvariable= self.frequency)
        self.entry_frq = Decimalentry(self.Frame1,textvariable= self.frequency)
        self.entry_frq['font'] = myFont
        self.entry_frq.place(x=280,y=220)

        self.label_proj = tk.Label(self.Frame1,text="Time step in attosecond ",bg="gray",fg="black")
        self.label_proj['font'] = myFont
        self.label_proj.place(x=10,y=260)

        #self.entry_proj = tk.Entry(self.Frame1,textvariable= self.ts)
        self.entry_ts = Decimalentry(self.Frame1,textvariable= self.ts)
        self.entry_ts['font'] = myFont
        self.ts.set(10)
        self.entry_ts.place(x=280,y=260)
        
        self.label_ns = tk.Label(self.Frame1,text="Number of Steps",bg="gray",fg="black")
        self.label_ns['font'] = myFont
        self.label_ns.place(x=10,y=300)

        #self.entry_proj = tk.Entry(self.Frame1,textvariable= self.ns)
        self.entry_ns = Onlydigits(self.Frame1, textvariable= self.ns)
        self.entry_ns['font'] = myFont
        self.ns.set(2000)
        self.entry_ns.place(x=280,y=300)
 
        Frame1_Button1 = tk.Button(self.Frame1, text="Back",activebackground="#78d6ff",command=lambda:self.back_button())
        Frame1_Button1['font'] = myFont
        Frame1_Button1.place(x=10,y=380)
        
        self.button_project = tk.Button(self.Frame1,text="Next",activebackground="#78d6ff",command=lambda:[self.choose_laser()])
        self.button_project['font'] = myFont
        self.button_project.place(x=350,y=380)

        self.button_project = tk.Button(self.Frame1,text="Laser Design",activebackground="#78d6ff",command=lambda:[self.laser_button()])
        self.button_project['font'] = myFont
        self.button_project.place(x=170,y=380)

        self.Frame2 = tk.Frame(self)
        self.Frame2.place(relx=0.480, rely=0.01, relheight=0.99, relwidth=0.492)

        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(cursor="fleur")

        self.label_pol_x = tk.Label(self.Frame2, text="Electric Polarisation in x axis", bg= "grey",fg="black")
        self.label_pol_x['font'] = myFont
        self.label_pol_x.place(x=10,y=60)
        
        pol_list = ["0","1"]
        self.entry_pol_x = ttk.Combobox(self.Frame2, textvariable= self.pol_x, value = pol_list)
        self.entry_pol_x['font'] = myFont
        self.entry_pol_x.insert(0,"0")
        self.entry_pol_x.place(x=280,y=60)
        self.entry_pol_x['state'] = 'readonly'

        self.label_pol_y = tk.Label(self.Frame2, text="Electric Polarisation in y axis", bg= "grey",fg="black")
        self.label_pol_y['font'] = myFont
        self.label_pol_y.place(x=10,y=110)
    
        self.entry_pol_y = ttk.Combobox(self.Frame2,textvariable= self.pol_y, value = pol_list)
        self.entry_pol_y['font'] = myFont
        self.entry_pol_y.insert(0,"0")
        self.entry_pol_y.place(x=280,y=110)
        self.entry_pol_y['state'] = 'readonly'

        self.label_pol_z = tk.Label(self.Frame2, text="Electric Polarisation in z axis", bg= "grey",fg="black")
        self.label_pol_z['font'] = myFont
        self.label_pol_z.place(x=10,y=160)
 
        self.entry_pol_z = ttk.Combobox(self.Frame2,textvariable= self.pol_z, value = pol_list)
        self.entry_pol_z['font'] = myFont
        self.entry_pol_z.insert(0,"0")
        self.entry_pol_z.place(x=280,y=160) 
        self.entry_pol_z['state'] = 'readonly'

        self.Frame2_Button1 = tk.Button(self.Frame2, state='disabled', text="Save Input",activebackground="#78d6ff", command=lambda:[self.save_button()])
        self.Frame2_Button1['font'] = myFont
        self.Frame2_Button1.place(x=10,y=380)

        self.label_msg = tk.Label(self.Frame2,text="")
        self.label_msg['font'] = myFont
        self.label_msg.place(x=10,y=350)
 
        self.Frame2_Button2 = tk.Button(self.Frame2, state='disabled', text="View Input",activebackground="#78d6ff", command=lambda:[self.view_button()])
        self.Frame2_Button2['font'] = myFont
        self.Frame2_Button2.place(x=170,y=380)
        
        self.Frame2_Button3 = tk.Button(self.Frame2, state='disabled', text="Run Job",activebackground="#78d6ff",command=lambda:self.run_job_button())
        self.Frame2_Button3['font'] = myFont
        self.Frame2_Button3.place(x=350,y=380)
        self.Frame3 = None


    def show_laser_plot(self, figure):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
        self.Frame3 = tk.Frame(self)
        self.Frame3.place(relx=0.480, rely=0.01, relheight=0.99, relwidth=0.492)

        self.Frame3.configure(relief='groove')
        self.Frame3.configure(borderwidth="2")
        self.Frame3.configure(relief="groove")
        self.Frame3.configure(cursor="fleur")

        self.Frame3.canvas = FigureCanvasTkAgg(figure, master=self.Frame3)
        self.Frame3.canvas.draw()
        self.Frame3.canvas.get_tk_widget().pack(side =tk.LEFT,fill='both', expand=True)
        self.Frame3.toolbar = NavigationToolbar2Tk(self.Frame3.canvas, self.Frame3)
        self.Frame3.toolbar.update()
        self.Frame3.canvas._tkcanvas.pack(side= tk.TOP,fill ='both')
    
    def laser_button(self):
        self.event_generate('<<DesignLaser>>')
   
    def activate_td_frame(self):
        self.Frame2.tkraise() 
        self.Frame2_Button1.config(state='active') 
        self.Frame2_Button2.config(state='active') 
        self.Frame2_Button3.config(state='active') 
               
    def destroy_plot(self):
        self.Frame3.destroy()

    def choose_laser(self):
        self.event_generate('<<ChooseLaser>>')


    def get_laser_pulse(self):
        laser_input = {

        "strength": self.strength.get(),
        "inval" :  self.inval.get(),
        "pol_x": self.pol_x.get(),
        "pol_y" : self.pol_y.get(),
        "pol_z" : self.pol_z.get(),
        "fwhm" :self.fwhm.get(),
        "frequency" :  self.frequency.get(),
        "time_step" : self.ts.get(),
        "number_of_steps": self.ns.get(),
        "tin" : self.tin.get()
        
        }
        return(laser_input)               

    def set_laser_design_dict(self, l_dict:dict):
        self.laser_design_dict = l_dict

    def get_parameters(self):
        
        from litesoph.utilities.units import au_to_fs,autime_to_eV
        laser_param = self.laser_design_dict               
        epol_list = [int(self.pol_x.get()),int(self.pol_y.get()),int(self.pol_z.get())]
       
        if self.engine == 'gpaw':
            abs_x = float(self.strength.get())*float(self.pol_x.get())
            abs_y = float(self.strength.get())*float(self.pol_y.get())
            abs_z = float(self.strength.get())*float(self.pol_z.get())
            abs_list = [abs_x, abs_y, abs_z]
            inp_list = [float(self.ts.get()),int(self.ns.get())]

            l_dict ={
                'frequency':self.frequency.get(),
                'strength':self.strength.get(),
                'sigma': round(autime_to_eV/self.laser_design_dict['sigma'], 2),
                'time0': round(self.laser_design_dict['time0']*au_to_fs, 2)
            }
            laser_param.update(l_dict)
            td_gpaw = {
                        'absorption_kick' :abs_list,
                        'propagate': tuple(inp_list),
                        'electric_pol': epol_list,             
                        'td_potential' : True,                     
                        'laser': laser_param}
            return td_gpaw
            
        elif self.engine == 'octopus':
            td_oct = {  'e_pol' :epol_list,
                        'max_step' : self.ns.get(),
                        'time_step': self.ts.get(),
                        'strength' : self.strength.get(),
                        'time0' :laser_param['time0'],
                        'sigma' : laser_param['sigma'],
                        'frequency': self.frequency.get()
                    }
                        
            return td_oct        
                      
        elif self.engine == 'nwchem':
            td_nwchem = { 'e_pol' :epol_list,
                          'tmax' : self.ns.get() * self.ts.get(),
                          'dt': self.ts.get(),
                          'max' : self.strength.get(),
                          'center' :laser_param['time0'],
                          'width' : laser_param['sigma'],
                          'freq': self.frequency.get()   
                        }

            print(td_nwchem)
            return td_nwchem

    def save_button(self):
        self.event_generate('<<SaveRT_TDDFT_LASERScript>>')          

    def view_button(self):
        self.event_generate('<<ViewRT_TDDFT_LASERScript>>')

    def run_job_button(self):
        self.event_generate('<<SubRT_TDDFT_LASER>>')

    def back_button(self):
        self.event_generate('<<ShowWorkManagerPage>>')

    def set_label_msg(self,msg):
        show_message(self.label_msg, msg) 

   

class PlotSpectraPage(tk.Frame):

    def __init__(self, parent, controller, engine, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.engine = engine
        
        self._default_var = {
            'del_e' : ['float', 0.05],
            'e_max' : ['float', 30.0],
            'e_min' : ['float']
        }
        self.gpaw_td_default = {
            'del_e' : ['float'],
            'e_max' : ['float'],
            'e_min' : ['float']
        }
        self.oct_td_default = {
            'del_e' : ['float'],
            'e_max' : ['float'],
            'e_min' : ['float']
        }
        self.nwchem_td_default= {
            'del_e' : ['float'],
            'e_max' : ['float'],
            'e_min' : ['float']
        }
        self._var = var_define(self._default_var)

        self.axis = tk.StringVar()

        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        j=font.Font(family ='Courier', size=20,weight='bold')
        k=font.Font(family ='Courier', size=40,weight='bold')
        l=font.Font(family ='Courier', size=15,weight='bold')
        
        self.Frame = tk.Frame(self) 
        
        self.Frame.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.978)
        self.Frame.configure(relief='groove')
        self.Frame.configure(borderwidth="2")
        self.Frame.configure(relief="groove")
        self.Frame.configure(cursor="fleur")
        
        self.heading = tk.Label(self.Frame,text="LITESOPH Spectrum Calculations and Plots", fg='blue')
        self.heading['font'] = myFont
        self.heading.place(x=350,y=10)
        
        self.label_pol = tk.Label(self.Frame, text= "Calculation of absorption spectrum:",bg= "grey",fg="black")
        self.label_pol['font'] = myFont
        self.label_pol.place(x=10,y=60)

        self.Frame2_Button_1 = tk.Button(self.Frame,text="Create input",activebackground="#78d6ff",command=self.create_button)
        self.Frame2_Button_1['font'] = myFont
        self.Frame2_Button_1.place(x=290,y=60)

        self.label_estep = tk.Label(self.Frame,text="Energy step (in eV)",bg="gray",fg="black")
        self.label_estep['font'] = myFont
        self.label_estep.place(x=10,y=100)

        self.entry_estep = tk.Entry(self.Frame,textvariable =self._var['del_e'])
        self.entry_estep['font'] = myFont
        self.entry_estep.place(x=300,y=100)

        self.label_emax = tk.Label(self.Frame,text="Minimum energy in the spectrum (in eV)",bg="gray",fg="black")
        self.label_emax['font'] = myFont
        self.label_emax.place(x=10,y=130)

        self.entry_emax = tk.Entry(self.Frame,textvariable =self._var['e_min'])
        self.entry_emax['font'] = myFont
        self.entry_emax.place(x=300,y=130)

        self.label_emax = tk.Label(self.Frame,text="Maximum energy in the spectrum (in eV)",bg="gray",fg="black")
        self.label_emax['font'] = myFont
        self.label_emax.place(x=10,y=160)

        self.entry_emax = tk.Entry(self.Frame,textvariable = self._var['e_max'])
        self.entry_emax['font'] = myFont
        self.entry_emax.place(x=300,y=160)

        self.label_msg = tk.Label(self.Frame, text= "",fg="black")
        self.label_msg['font'] = myFont
        self.label_msg.place(x=420,y=60)

        self.Frame2_Run = tk.Button(self.Frame,text="Run Job",activebackground="#78d6ff",command=lambda:[self.event_generate('<<SubSpectrum>>')])
        self.Frame2_Run['font'] = myFont
        self.Frame2_Run.place(x=320,y=380)
    
        Frame_Button1 = tk.Button(self.Frame, text="Back",activebackground="#78d6ff",command=lambda:self.event_generate('<<ShowWorkManagerPage>>'))
        Frame_Button1['font'] = myFont
        Frame_Button1.place(x=10,y=380)

        #self.show_plot()

    # def show_plot(self):
    #     check = self.controller.status.check_status('spectra', 2)
    #     if check is True:
    #         self.create_plot()  
    #     else:
    #         pass  

    def get_parameters(self):
        td_dict_gp = {
            'del_e':self._var['del_e'].get(),
            'e_max':self._var['e_max'].get(),
            'e_min': self._var['e_min'].get()       
        }
        
        td_dict_oct = {
            'del_e':self._var['del_e'].get(),
            'e_max':self._var['e_max'].get(),
            'e_min': self._var['e_min'].get()
          }

        td_dict_nwchem = {
            }
        
        if self.engine == 'gpaw':
            return td_dict_gp
        elif self.engine == 'nwchem':
            return td_dict_nwchem
        elif self.engine == 'octopus':
            return td_dict_oct            

    def create_plot(self):
        myFont = font.Font(family='Helvetica', size=10, weight='bold')
        
        self.label_pol = tk.Label(self.Frame, text="Select the axis", bg= "grey",fg="black")
        self.label_pol['font'] = myFont
        self.label_pol.place(x=10,y=130)

        ax_pol = ["x","y","z"]
        self.entry_pol_x = ttk.Combobox(self.Frame, textvariable= self.axis, value = ax_pol, width= 15)
        self.entry_pol_x['font'] = myFont
        self.entry_pol_x.insert(0,"x")
        self.entry_pol_x.place(x=160,y=130)
        self.entry_pol_x['state'] = 'readonly'
        
        # self.Frame2_Plot = tk.Button(self.Frame,text="Plot",activebackground="#78d6ff",command=lambda:[plot_spectra(self.returnaxis(),str(self.controller.directory)+'/Spectrum/spec.dat',str(self.controller.directory)+'/Spectrum/spec.png','Energy (eV)','Photoabsorption (eV$^{-1}$)', None)])
        # self.Frame2_Plot['font'] = myFont
        # self.Frame2_Plot.place(x=320,y= 130)
    
    def returnaxis(self):
        if self.axis.get() == "x":
            axis = 1
        if self.axis.get() == "y":
            axis = 2
        if self.axis.get() == "z":
            axis = 3
        return axis

    def create_button(self):
        print('view')
        self.event_generate('<<CreateSpectraScript>>')

    # def createspec(self, engn):
    #     spec_dict = {}
    #     spec_dict['moment_file'] = pathlib.Path(self.controller.directory) / "TD_Delta" / "dm.dat"
    #     # spec_dict['spectrum_file'] = pathlib.Path(self.controller.directory) / "Spectrum"/ specfile
    #     job = Spectrum(spec_dict,  engine.EngineGpaw(), str(self.controller.directory),'spec') 
    #     job.write_input()
    #     self.controller.task = job
    #     self.controller.check = True
    #     self.controller.status.update_status('spectra', 1)
    #     show_message(self.label_msg, "Saved")
    #     self.Frame2_Run.config(state='active')
      

class DmLdPage(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        
        from litesoph.utilities.units import au_to_fs
        self.plot_task = tk.StringVar()
        self.compo = tk.StringVar()

        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        j=font.Font(family ='Courier', size=20,weight='bold')
        k=font.Font(family ='Courier', size=40,weight='bold')
        l=font.Font(family ='Courier', size=15,weight='bold')
        
        self.Frame = tk.Frame(self) 
        
        self.Frame.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.978)
        self.Frame.configure(relief='groove')
        self.Frame.configure(borderwidth="2")
        self.Frame.configure(relief="groove")
        self.Frame.configure(cursor="fleur")
        
        self.heading = tk.Label(self.Frame,text="LITESOPH Dipole Moment and laser Design", fg='blue')
        self.heading['font'] = myFont
        self.heading.place(x=350,y=10)
        
        self.label_pol = tk.Label(self.Frame, text= "Plot:",bg= "grey",fg="black")
        self.label_pol['font'] = myFont
        self.label_pol.place(x=10,y=60)

        plot_list = ["Dipole Moment", "Dipole Moment and Laser"]
        self.entry_pol_x = ttk.Combobox(self.Frame,textvariable=self.plot_task, value = plot_list, width = 25)
        self.entry_pol_x['font'] = myFont
        self.entry_pol_x.insert(0,"Dipole Moment")
        self.entry_pol_x.place(x=280,y=60)
        self.entry_pol_x['state'] = 'readonly'

        #self.label_pol = Label(self.Frame, text= "Axis of Electric polarization:",fg="black")
        #self.label_pol['font'] = myFont
        #self.label_pol.place(x=10,y=110)

        self.label_pol = tk.Label(self.Frame, text="Select the axis", bg= "grey",fg="black")
        self.label_pol['font'] = myFont
        self.label_pol.place(x=10,y=110)

        com_pol = ["x component","y component","z component"]
        self.entry_pol_x = ttk.Combobox(self.Frame, textvariable= self.compo, value = com_pol, width= 25)
        self.entry_pol_x['font'] = myFont
        self.entry_pol_x.insert(0,"x component")
        self.entry_pol_x.place(x=280,y=110)
        self.entry_pol_x['state'] = 'readonly'

        self.Frame2_Button_1 = tk.Button(self.Frame,text="Plot",activebackground="#78d6ff", command=lambda:[self.plot_button()])
        self.Frame2_Button_1['font'] = myFont
        self.Frame2_Button_1.place(x=250,y=380)
    
        Frame_Button1 = tk.Button(self.Frame, text="Back",activebackground="#78d6ff",command=lambda:self.event_generate('<<ShowWorkManagerPage>>'))
        Frame_Button1['font'] = myFont
        Frame_Button1.place(x=10,y=380)
        
    def returnaxis(self):
        if self.compo.get() == "x component":
            axis = 2
        if self.compo.get() == "y component":
            axis = 3
        if self.compo.get() == "z component":
            axis = 4
        return axis

    def plot_button(self):
        from litesoph.utilities.units import au_to_fs
        if self.plot_task.get() == "Dipole Moment":
            plot_spectra(self.returnaxis(),str(self.controller.directory)+'/TD_Laser/dmlaser.dat',str(self.controller.directory)+'/TD_Laser/dmlaser.png',"Time (fs)","Dipole moment (au)", au_to_fs)
        if self.plot_task.get() == "Dipole Moment and Laser":
            plot_files(str(self.controller.directory)+'/laser.dat',str(self.controller.directory)+'/TD_Laser/dmlaser.dat',1, self.returnaxis())
   
class TcmPage(tk.Frame):

    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        
        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        self.min = tk.DoubleVar()
        self.max = tk.DoubleVar()
        self.step = tk.DoubleVar()
        self.freq = tk.DoubleVar()

        j=font.Font(family ='Courier', size=20,weight='bold')
        k=font.Font(family ='Courier', size=40,weight='bold')
        l=font.Font(family ='Courier', size=15,weight='bold')

        self.Frame = tk.Frame(self)
        
        self.Frame.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.978)
        self.Frame.configure(relief='groove')
        self.Frame.configure(borderwidth="2")
        self.Frame.configure(relief="groove")
        self.Frame.configure(cursor="fleur")
        
        self.heading = tk.Label(self.Frame,text="LITESOPH Kohn Sham Decomposition", fg='blue')
        self.heading['font'] = myFont
        self.heading.place(x=350,y=10)

        self.FrameTcm2_label_path = tk.Label(self.Frame,text="Frequency space density matrix",fg="blue")
        self.FrameTcm2_label_path['font'] = myFont
        self.FrameTcm2_label_path.place(x=10,y=50)

        self.Label_freqs = tk.Label(self.Frame,text="List of the Frequencies obtained from the photoabsorption \nspectrum (in eV) at which Fourier transform of density matrix is sought.\n(Entries should be separated by space,eg: 2.1  4)",fg="black", justify='left')
        self.Label_freqs['font'] = myFont
        self.Label_freqs.place(x=10,y=80)
        
        self.TextBox_freqs = tk.Text(self.Frame, height=4, width=60)
        self.TextBox_freqs['font'] = myFont
        self.TextBox_freqs.place(x=10,y=150)

        #self.Label_freqs = Label(self.Frame,text="Or provide a range as <min value>-<max value>-<step size> respectively",fg="black")
        #self.Label_freqs['font'] = myFont
        #self.Label_freqs.place(x=10,y=240)
 
        #self.Tcm_entry_ns = Entry(self.Frame, textvariable=self.min)
        #self.Tcm_entry_ns['font'] = myFont
        #self.Tcm_entry_ns.place(x=10,y=280)
       
        #self.Tcm_entry_ns = Entry(self.Frame, textvariable= self.max)
        #self.Tcm_entry_ns['font'] = myFont
        #self.Tcm_entry_ns.place(x=200,y=280)
      
        #self.Tcm_entry_ns = Entry(self.Frame, textvariable=self.step, width= 10)
        #self.Tcm_entry_ns['font'] = myFont
        #self.Tcm_entry_ns.place(x=390,y=280)

        Frame_Button1 = tk.Button(self.Frame, text="Back",activebackground="#78d6ff",command=lambda:self.event_generate('<<ShowWorkManagerPage>>'))
        Frame_Button1['font'] = myFont
        Frame_Button1.place(x=10,y=380)

        #self.buttonRetrieve = Button(self.Frame, text="Retrieve Freq",activebackground="#78d6ff",command=lambda:[self.retrieve_input(),self.freq_listbox(), self.tcm_button()])
        self.buttonRetrieve = tk.Button(self.Frame, text="Create input",activebackground="#78d6ff",command=lambda:self.create_tcm())
        self.buttonRetrieve['font'] = myFont
        self.buttonRetrieve.place(x=200,y=380)

        self.Frame_run = tk.Button(self.Frame,text="Run Job", state= 'disabled',activebackground="#78d6ff", command=lambda:[self.event_generate('<<ShowJobSubmissionPage>>')])
        self.Frame_run['font'] = myFont
        self.Frame_run.place(x=360,y=380)
        
    def retrieve_input(self):
        inputValues = self.TextBox_freqs.get("1.0", "end-1c")
        freqs = inputValues.split()

        self.freq_list = []
        for freq in freqs[0:]:
            self.freq_list.append(float(freq))
        return(self.freq_list)   
    
    def create_tcm(self):
        self.retrieve_input()
        gs = pathlib.Path(self.controller.directory) / "GS" / "gs.gpw"
        wf = pathlib.Path(self.controller.directory) / "TD_Delta" / "wf.ulm"
        tcm_dict = {
                'gfilename' : gs,
                'wfilename' : wf,
                'frequencies' : self.freq_list,
                'name' : "x"
                 }         
        self.job = TCM(tcm_dict, engine.EngineGpaw(), self.controller.directory,  'tcm')
        self.job.write_input()
        self.controller.task = self.job 
        self.controller.check = False
        self.Frame_run.config(state= 'active')      

    def freq_listbox(self):
        myFont = font.Font(family='Helvetica', size=10, weight='bold')
        self.plot_label= tk.Label(self.Frame,text="Select the frequency and Plot",fg="black", bg="gray")
        self.plot_label['font'] = myFont
        self.plot_label.place(x=560,y=70)

        self.listbox = tk.Listbox(self, font=myFont)
        self.listbox.place(x = 580, y=100)        
        for item in self.freq_list:
            self.listbox.insert(tk.END, item)
        self.plot_button = tk.Button(self.Frame, text="Plot",activebackground="#78d6ff",command=lambda:self.freq_plot())
        self.plot_button['font'] = myFont
        self.plot_button.place(x=740,y=200)   

    def freq_plot(self):
        for i in self.listbox.curselection():
            self.tcm.plot(self.tcm_dict, i)  

class JobSubPage(tk.Frame):

    def __init__(self, parent, task, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.task = task
        self.runlocal_np =  None
        self.run_script_path = None

        myFont = font.Font(family='Helvetica', size=10, weight='bold')
        j=font.Font(family ='Courier', size=20,weight='bold')
        k=font.Font(family ='Courier', size=40,weight='bold')
        l=font.Font(family ='Courier', size=15,weight='bold')
        self.myfont = myFont
        self.Frame1 = tk.Frame(self)
        self.processors = tk.IntVar()
        self.ip = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.rpath = tk.StringVar()

        self.Frame1.place(relx=0.01, rely=0.01, relheight=0.25, relwidth=0.978)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(cursor="fleur")

        sbj_label1 = tk.Label(self.Frame1, text="LITESOPH Local Job Submission", fg='blue')
        sbj_label1['font'] = myFont
        sbj_label1.place(x=350,y=10)

        sbj_label1 = tk.Label(self.Frame1, text="Number of processors", bg='gray', fg='black')
        sbj_label1['font'] = myFont
        sbj_label1.place(x=15,y=50)

        sbj_entry1 = tk.Entry(self.Frame1,textvariable= self.processors, width=20)
        self.processors.set(1)
        sbj_entry1['font'] = l
        sbj_entry1.place(x=200,y=50)
        
        #sbj_label1 = Label(self.Frame2, text="To submit job through Network, provide details", bg='gray', fg='black')
        #sbj_label1['font'] = myFont
        #sbj_label1.place(x=15,y=110)

        self.sbj_button1 = tk.Button(self.Frame1, text="Run Local",activebackground="#78d6ff",command=lambda:[self.submitjob_local()])
        self.sbj_button1['font'] = myFont
        self.sbj_button1.place(x=600, y=50)

        self.msg_label1 = tk.Label(self.Frame1, text='', fg='blue')
        self.msg_label1['font'] = myFont
        self.msg_label1.place(x=700,y=55)

        self.Frame2 = tk.Frame(self)
        self.Frame2.place(relx=0.01, rely=0.26, relheight=0.60, relwidth=0.978)
        
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(cursor="fleur")

        sbj_label1 = tk.Label(self.Frame2, text="LITESOPH Network Job Submission", fg='blue')
        sbj_label1['font'] = myFont
        sbj_label1.place(x=340,y=10)
        
        sbj_label1 = tk.Label(self.Frame2, text= "Host IP address", bg='gray', fg='black')
        sbj_label1['font'] = myFont
        sbj_label1.place(x=15,y=50)
 
        sbj_entry1 = tk.Entry(self.Frame2,textvariable= self.ip, width=20)
        sbj_entry1['font'] = l
        sbj_entry1.place(x=200,y=50)

        sbj_label1 = tk.Label(self.Frame2, text= "User Name", bg='gray', fg='black')
        sbj_label1['font'] = myFont
        sbj_label1.place(x=15,y=100)

        sbj_entry1 = tk.Entry(self.Frame2,textvariable= self.username, width=20)
        sbj_entry1['font'] = l
        sbj_entry1.place(x=200,y=100)
 
        sbj_label1 = tk.Label(self.Frame2, text= "Password", bg='gray', fg='black')
        sbj_label1['font'] = myFont
        sbj_label1.place(x=15,y=150)

        sbj_entry1 = tk.Entry(self.Frame2,textvariable= self.password, width=20, show = '*')
        sbj_entry1['font'] = l
        sbj_entry1.place(x=200,y=150)

        sbj_label1 = tk.Label(self.Frame2, text= "Remote Path", bg='gray', fg='black')
        sbj_label1['font'] = myFont
        sbj_label1.place(x=15,y=200)

        sbj_entry1 = tk.Entry(self.Frame2,textvariable= self.rpath, width=20)
        sbj_entry1['font'] = l
        sbj_entry1.place(x=200,y=200)
      
        #sbj_button2 = Button(self.Frame2, text="Create Job Script",activebackground="#78d6ff")
        #sbj_button2['font'] = myFont
        #sbj_button2.place(x=600, y=60)
         
        #sbj_button2 = Button(self.Frame2, text="Upload Job Script",activebackground="#78d6ff",command =lambda:[self.open_file(self.controller.directory),show_message(self.message_label,"Uploaded")])
        sbj_button2 = tk.Button(self.Frame2, text="Upload Job Script",activebackground="#78d6ff",command = self.upload_script)
        sbj_button2['font'] = myFont
        sbj_button2.place(x=600, y=150)
  
        self.message_label = tk.Label(self.Frame2, text='', foreground='red')
        self.message_label['font'] = myFont
        self.message_label.place(x=800,y=155)

        sbj_button2 = tk.Button(self.Frame2, text="Run Job Network",activebackground="#78d6ff", command=lambda:[self.submitjob_network()])
        sbj_button2['font'] = myFont
        sbj_button2.place(x=600, y=200)
 
        self.Frame3 = tk.Frame(self)
        self.Frame3.place(relx=0.01, rely=0.86, relheight=0.12, relwidth=0.978)

        self.Frame3.configure(relief='groove')
        self.Frame3.configure(borderwidth="2")
        self.Frame3.configure(relief="groove")
        self.Frame3.configure(cursor="fleur")

        back2prev = tk.Button(self.Frame3, text="Back",activebackground="#78d6ff",command=lambda:self.event_generate('<<ClickBackButton>>'))
        back2prev['font'] = myFont
        back2prev.place(x=15,y=10)

        back = tk.Button(self.Frame3, text="Back to main page",activebackground="#78d6ff",command=lambda:[self.event_generate('<<ShowWorkManagerPage>>')])
        back['font'] = myFont
        back.place(x=600,y=10)      

    def show_output_button(self, txt, name):
        self.plot_button1 = tk.Button(self.Frame1, text=txt,activebackground="#78d6ff",command=lambda:[self.event_generate(f'<<Output{name}>>')])
        self.plot_button1['font'] = self.myfont
        self.plot_button1.place(x=800, y=50)        

    def get_processors(self):
        return self.processors.get()

    def submitjob_local(self):
        event = '<<Run'+self.task+'Local>>'
        self.event_generate(event)

    def disable_run_button(self):
        self.sbj_button1.config(state='disabled')

    def activate_run_button(self):
        self.sbj_button1.config(state='active')

    #     if self.controller.check is not True:
    #         from litesoph.utilities.job_submit import get_submit_class
    #         self.submit = get_submit_class(engine=self.task.engine, configs=self.controller.lsconfig, nprocessors=self.processors.get())
    #         process = self.task.run(self.submit)
    #     else:
    #         from litesoph.gui.job_validation import select_job
    #         job = self.checkjob()
    #         select_job(self,job, self.controller.status)     
        

    # def checkjob(self):
    #     try:
    #         if type(self.controller.task).__name__ == 'GroundState':
    #             return('gs')
    #         if type(self.controller.task).__name__ == 'RT_LCAO_TDDFT':
    #             return self.controller.task.keyword  
    #         if type(self.controller.task).__name__ == 'Spectrum':
    #             return('spec')
    #         if type(self.controller.task).__name__ == 'TCM':
    #             return('tcm')
    #         if type(self.controller.task).__name__ == 'InducedDensity':
    #             return('indensity')
    #     except:
    #         messagebox.showerror(message="Input not created!. Please create input before submitting the job ")

    # def call_run(self,key, value):
    #     from litesoph.utilities.job_submit import get_submit_class
    #     self.submit = get_submit_class(engine=self.task.engine, configs=self.controller.lsconfig, nprocessors=self.processors.get())
    #     process = self.task.run(self.submit)
    #     f = tk.file_check(self.job_d['check_list'], self.controller.directory) 
    #     f_check = f.check_list(self.job_d['out']) 
    #     if f_check is True:
    #         self.controller.status.update_status(key, value) 
    #         show_message(self.msg_label1,"Job Done")
    #     else:
    #         show_message(self.msg_label1, "Error while generating output") 
            
   
    # def run_job(self, key, value1, value2):
    #     if self.job_d['cal_check'] is False:
    #         self.call_run(key, value1)  
    #     else:
    #         show_message(self.msg_label1, "")
    #         check_yn = messagebox.askyesno(title="Job is done",message="Do you want to redo the calculation? ")
    #         if check_yn is True:
    #             self.controller.status.update_status(key, value2)
    #             self.call_run(key, value1)

    def upload_script(self):

        top1 = tk.Toplevel()
        top1.geometry("600x500")
        top1.title("LITESOPH Job Script Viewer")

        cores_1 = tk.StringVar()

        myFont = font.Font(family='Helvetica', size=10, weight='bold')

        j=font.Font(family ='Courier', size=20,weight='bold')
        k=font.Font(family ='Courier', size=40,weight='bold')
        l=font.Font(family ='Courier', size=15,weight='bold')
        
        text_scroll =tk.Scrollbar(top1) 
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        my_Text = tk.Text(top1, width = 78, height = 25, yscrollcommand= text_scroll.set)
        my_Text['font'] = myFont
        my_Text.place(x=15,y=60)
        #if selectedfile is not None:
            #self.inserttextfromfile(selectedfile, my_Text)
            #self.current_file = selectedfile

        text_scroll.config(command= my_Text.yview)
        
        #def inserttextfromfile(self, filename, my_Text):
            #text_file = open(filename, 'r')
            #stuff = text_file.read()
            #my_Text.insert(END,stuff)
            #text_file.close()

        view = tk.Button(top1, text="Select Script",activebackground="#78d6ff",command=lambda:[self.open_txt(my_Text)])
        view['font'] = myFont
        view.place(x=100,y=450)

        save = tk.Button(top1, text="Save",activebackground="#78d6ff",command=lambda:[self.save_txt(my_Text)])
        save['font'] = myFont
        save.place(x=280, y=450)
        
        close = tk.Button(top1, text="Close", activebackground="#78d6ff",command=top1.destroy)
        close['font'] = myFont
        close.place(x=400,y=450)
        
    def open_txt(self,my_Text):
            self.run_script_path = filedialog.askopenfilename(initialdir="./", title="Select File", filetypes=(("All files","*.*"),))
            #text_file_name = open_file(user_path) 
            self.current_file = self.run_script_path
            text_file = open(self.run_script_path, 'r')
            stuff = text_file.read()
            my_Text.insert(tk.END,stuff)
            text_file.close()     

    def save_txt(self,my_Text):
            text_file = self.current_file
            text_file = open(text_file,'w')
            text_file.write(my_Text.get(1.0, tk.END))
    
    def submitjob_network(self):
        event = '<<Run'+self.task+'Network>>'
        self.event_generate(event)
        
    def get_network_dict(self):

        network_job_dict = {
          'ip':self.ip.get(),
          'username':self.username.get(),
          'password':self.password.get(),
          'remote_path':self.rpath.get(),
            } 
        return network_job_dict

class TextViewerPage(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.save_txt = None
        self.task_name = None
        myFont = tk.font.Font(family='Helvetica', size=10, weight='bold')

        j=tk.font.Font(family ='Courier', size=20,weight='bold')
        k=tk.font.Font(family ='Courier', size=40,weight='bold')
        l=tk.font.Font(family ='Courier', size=15,weight='bold')

        self.Frame = tk.Frame(self)

        self.Frame.place(relx=0.01, rely=0.01, relheight=0.99, relwidth=0.98)
        self.Frame.configure(relief='groove')
        self.Frame.configure(borderwidth="2")
        self.Frame.configure(relief="groove")
        self.Frame.configure(cursor="fleur")
  
        self.FrameTcm1_label_path = tk.Label(self, text="LITESOPH Text Viewer",fg="blue")
        self.FrameTcm1_label_path['font'] = myFont
        self.FrameTcm1_label_path.place(x=400,y=10)

        
        text_scroll =tk.Scrollbar(self)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_view = tk.Text(self, width = 130, height = 20, yscrollcommand= text_scroll.set)
        self.text_view['font'] = myFont
        self.text_view.place(x=15,y=60)

        text_scroll.config(command= self.text_view.yview)

        save = tk.Button(self, text="Save",activebackground="#78d6ff",command=self.save)
        save['font'] = myFont
        save.place(x=320, y=380)

        back = tk.Button(self, text="Back",activebackground="#78d6ff",command=lambda:[self.back_button()])
        back['font'] = myFont
        back.place(x=30,y=380)
    
    def set_task_name(self, name):
        self.task_name = name
   
    def insert_text(self, text):
        self.text_view.insert(tk.END, text)
 
    def save(self):
        self.save_txt = self.text_view.get(1.0, tk.END)
        self.event_generate(f'<<Save{self.task_name}>>')
    
    def back_button(self):
        self.event_generate(f'<<View{self.task_name}Page>>')

class View_Text(tk.Frame):
    """ Text_View class with grid options"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent,*args, **kwargs)

        myFont = tk.font.Font(family='Helvetica', size=10, weight='bold')

        text_scroll =tk.Scrollbar(self)
        text_scroll.grid(row=0, column=1, sticky='nsew' )
        #text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        #self.text_view = tk.Text(self, width = 130, height = 20, yscrollcommand= text_scroll.set)
        self.text_view = tk.Text(self, yscrollcommand= text_scroll.set)
        self.text_view['font'] = myFont
        self.text_view.grid(row=0, column=0, padx=5, pady=5)
        text_scroll.config(command=self.text_view.yview)        
    
    def clear_text(self):
        self.text_view.delete("1.0", tk.END)

    def insert_text(self, text):
        self.text_view.configure(state='normal')
        self.clear_text()
        
        self.text_view.insert(tk.END, text)
        self.text_view.configure(state='disabled')