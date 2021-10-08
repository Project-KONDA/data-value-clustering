'''text popup for context menu, used as help'''
from tkinter import *

from gui_general.scrollable_frame import create_scrollable_frame


def menu_help_result(master):
    """help popup for Clustering Result & Evaluation view"""
    text = [
        "The Clustering Result & Evaluation view provides information on the calculated clustering and supports you validating it. In the top left, quantitative meta-information on the calculated clustering are given.",
        "",
        ["MDS Scatter Plot"],
        "Below, the MDS Scatter Plot gives an overview of the clustering. Each dot represents an abstracted data value. The distances between the dots represent the dissimilarities between the abstracted data values. Therefore, the closer the dots are, the similar the values are. Each cluster is represented by a different colour. The noisy values are presented as black dots. This plot allows you to quickly get an overview of the compactness and separation of the clustering.",
        "A clustering is compact if there is a high similarity within clusters and it is separate if there is a low similarity between clusters. In general, a good clustering should have high compactness and separation. If the colours are very mixed, this may hint at the low meaningfulness of the clustering (cf. evaluation question 1). The plot may also assist you in answering evaluation question 2. But make sure to also check the entire clustering provided as an Excel file before answering the questions.",
        "",
        ["Clustering"],
        "Most importantly, you can access the complete clustering provided in an Excel file via the green button below. If the excel file is not created, you first must specify the save path.",
        "",
        "The Excel file contains three sheets, that present the clutering:",
        " • The first one shows the clustering of the original values.",
        " • The second one shows the clustering of the abstracted values by means of original values as representatives.",
        " • The third sheet additionally shows the variance within each cluster and the dissimilarity of each value to the others in the same cluster.",
        "An extremely high variance within a cluster indicates that you should consider analysing this cluster separately (cf. evaluation question 4) as it may be too heterogeneous to oversee the types of contained values. You should further take a look at values with an extremely high dissimilarity to the other values in the same cluster, as they may be significantly different from those.",
        "",
        ["Evaluation"],
        "After having familiarized yourself with the clustering, you need to validate the clustering, i.e. find out whether you are satisfied with the clustering or need another iteration with a modified configuration. The evaluation questionnaire given on the right-hand side supports this process.",
        "In case you are not satisfied with the clustering, we calculate suggestions for modifications of the configuration of the next iteration. The suggestions are given in the configuration views in blue text.",
        "",
        ["Confirm & Discard"],
        "To confirm your evaluation answers, press the 'OK' button.",
        "To discard your evaluation answers, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, "Clustering Result & Evaluation - Help", text)


def menu_help_clustering_configuration(master):
    """help popup for Clustering Parameter Configuration view"""
    text = [
        "The Clustering Parameter Configuration view allows you to specify the parameter values for the chosen clustering algorithm.",
        "",
        ["Parameters"],
        "All parameters that can be specified are listed and brief explanations are given below the title. You can specify the parameter values via three types of input:",
        " • via sliders (for numerical values)",
        " • via radio buttons (for enumerations)",
        " • via check boxes (for booleans)",
        "",
        ["Assistance"],
        "The values that are specified per default can serve as a good starting point for your first iteration. To reset the parameter value to the default value, press the 'Reset' button. For some parameters, a plot showing fitting information is provided when pressing the 'Show plot' button.",
        "For enumerations, recommended options are highlighted in light green, while options that are rather not recommended are highlighted in light red.",
        "",
        ["Optional"],
        "Some parameters are optional or only used under specific circumstances. When they are not used, they are greyed out. Optional parameters and be enabled and disabled via a checkbox on the left-hand side.",
        "",
        ["Dependencies"],
        "In some cases, there are dependencies between the parameters. They are ensured automatically:",
        "Some dependencies result in the (de-)activation or the modification of the range of values of other parameters.",
        "",
        ["Confirm & Discard"],
        "To confirm your configuration, press the 'OK' button.",
        "To discard your configuration, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, "Clustering Parameter Configuration - Help", text)


def menu_help_clustering_selection(master):
    """help popup for Clustering Algorithm Selection view"""
    text = [
        "The Clustering Algorithm Selection view allows you to choose a clustering algorithm.",
        "",
        ["Questionnaire"],
        "To have a reference point, which algorithm is the most fitting for your purpose, we offer a short questionnaire on the left-hand side.",
        "",
        ["Algorithm Selection"],
        "Depending on your answers, the list of fitting algorithms shown on the right-hand side is updated dynamically.",
        "",
        ["Confirm & Discard"],
        "To confirm your selection, press the 'OK' button.",
        "To discard your selection, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, "Clustering Algorithm Selection - Help", text)


def menu_help_cost_map(master):
    """help popup for Dissimilarity Configuration - Matrix view"""
    text = [
        "The Matrix View is a view for the Configuration of the Dissimilarities between values. It gives you full control over the weights used in the calculation of dissimilarities between data values. That means you assign numerical values to the distance between groups of values. The weights represent the dissimilarities between the specified character groups. This matrix can be read as single transformations from a character out of the group specified in the left column to a character from the group in the top row. You should specify these weights based on your domain knowledge, which means based on your understanding of how different the characters are in the context of the data field that you want to analyse.",
        "",
        ["Character Groups"],
        "The left input fields represent groups of characters. Please enumerate all characters, that should be in the group. Note, that the interface supports sequences like 'a-z' or 'A-Z' for letters and '0-9' for digits. Only the first occurrence of a character in one of the groups is relevant. The last row and column represent all characters not mentioned in the lines above.",
        "You are free to modify the character groups. The default groups are automatically derived from the abstraction configuration. You also can add new groups i.e. lines via the '+' button or remove the last group via the '-' button. To reset the groups correspondingly, press the 'Reset' button.",
        "",
        "Note that some characters represent features that were removed by the abstraction. For example, depending on the abstraction configuration, '1' may represent any integer. This mapping between characters and the represented features that were abstracted is provided in the second column.",
        "",
        ["Weights"],
        "You must enter the weights of character deletions (first column), insertions (first row) and substitution (rest of the matrix) as numbers. The first column and row represent the empty string. Here the weights of deleting and inserting the corresponding character are entered. The weight in row i and column j represents the weight for substituting the characters represented by row i by characters represented by column j. Only the relative size of the weights matters. The dissimilarity measure between two values shall be symmetrical. That means the distance from value A to value B is the same as from B to A. Because of this, the matrix is mirrored on the diagonal. The entry fields above the diagonal are read-only.",
        "Higher weights for a character group mean more dissimilarity caused by the deletion/insertion/substitution of these characters. Therefore, you should choose higher weights for characters that you do not expect to find regularly in the data values and for characters that may cause great dissimilarity of the data values.",
        "",
        ["Confirm, Reset & Discard"],
        "To confirm your modifications of the weights, press the 'OK' button.",
        "To reset character groups, press the 'Reset' button.",
        "To discard your modifications, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, "Dissimilarity Configuration - Matrix - Help", text)


def menu_help_blob_input(master):
    """help popup for Dissimilarity Configuration - Blobs view"""
    text = [
        "The Blob View is a view for the Configuration of the Dissimilarities between values. It allows you to configure the weights used in the calculation of dissimilarities between data values by moving and scaling graphical objects on a 2D canvas.",
        "The weights represent the dissimilarities between character groups. You should specify these weights based on your domain knowledge, which means based on your understanding on how different the characters are in the context of the data field that you want to analyse.",
        "",
        ["Blobs"],
        "Each of the spheres (we call them 'blobs') in this diagram represent a group of similar characters. This group of characters is described in the label. There is one empty blue blob. This represents an empty text. The character groups are automatically derived from your configuration of the abstraction.",
        "",
        ["Distance"],
        "The distances between blobs represent the weight of replacing corresponding characters. The weight of deleting and inserting a character is represented by the distance to the special empty blue blob.",
        # interpretation
        "When the blobs just barely touch each other, the dissimilarity between them is interpreted as the value 1.",
        # controls
        "The distances can be modified via Drag & Drop.",
        "",
        "Higher weights for a character group mean more dissimilarity caused by the deletion/insertion/substitution of these characters. You should choose higher weights for characters that you do not expect to find regularly in the data values and for characters that may cause great dissimilarity of the data values.",
        "",
        ["Size"],
        "The size of each blob represents the weight of substituting characters of the represented group by each other. Some blobs cannot be scaled. These are on default fixed on the minimal size and are slightly less saturated. The fixed blobs depend on your configuration of the abstraction.",
        # interpretation
        "The minimum size represents the value 0. The default size is 1.",
        # controls
        "The size of not fixed blobs can be changed via the scroll wheel while the mouse hovers over the blob. The default size can be restored by pressing N (for 'normalize') on mouseover.",
        "",
        ["Confirm, Reset & Discard"],
        "To confirm your modifications of the weights, press the 'OK' button.",
        "To reset the position of the blobs, press the 'Reset' button.",
        "To discard your modifications, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, "Dissimilarity Configuration - Blobs - Help", text)


def menu_help_distance_slider(master):
    """help popup for Dissimilarity Configuration - Sliders view"""
    text = [
        "The Sliders view allows configuring the calculation of Dissimilarities between data values. More precisely, you weight the influence of certain characters or character sequences on the dissimilarity between data values in which they occur. These weights are specified via sliders. You should choose the weights based on your domain knowledge about the data field analysed.",
        "",
        ["Character Groups"],
        "The Sliders view allows configuring the calculation of Dissimilarities between data values. More precisely, you weight the influence of certain characters or character sequences on the dissimilarity between data values in which they occur. These weights are specified via sliders. You should choose the weights based on your domain knowledge about the data field analysed.",
        "When activating 'Custom Character Groups', another column appears on the left-hand side containing an entry field per group. This column allows you to modify the groups. Here abstracted features are not represented by the descriptive label but by the single character to which they were abstracted. The meaning of these characters is indicated by the middle column. Again, the tooltips provide explanations. You can move characters between die entry fields to move them between groups. Note that only the first occurrence of a character in one of the groups is relevant. Rows with empty entries will be ignored. Characters which are not present in the abstracted data values are ignored. The last line represents all characters not mentioned in the previous lines. You can add and remove groups, i.e. lines, via the '+' and '-' buttons.  The default groups are automatically derived from the abstraction configuration and serve as a good starting point. To reset the groups correspondingly, press the 'Reset' button.",
        "",
        ["Weights"],
        "Per group, you can specify the weight via the slider given on the right-hand side. This input method is limited such that you only specify the relative influence of characters (and character sequences) on the dissimilarity between data values. Thus, higher weights for a group mean more dissimilarity caused by the presence of these characters in data values. A weight of zero means these characters do not have any influence on the dissimilarity. You should choose higher weights for characters that you do not expect to find regularly in the data values and for characters that may cause great dissimilarity of the data values.",
        "To specify the weights more flexibly, choose Expert Mode.",
        "",
        ["Confirm & Discard"],
        "To confirm your modifications of the weights, press the 'OK' button.",
        "To discard your modifications, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, "Dissimilarity Configuration - Sliders - Help", text)


def menu_help_distance_choice(master):
    """help popup for Dissimilarity Configuration Method Selection view"""
    text = [
        "The Dissimilarity Configuration Method Selection view allows you to select a method for configuring the dissimilarity calculation, i.e. for weighting the similarity between character groups based on your domain knowledge. Currently, only the weighted Levenshtein distance is supported and can be configured via 3 different methods. The easier methods allow less flexibility. But as in most cases, the easiest method is sufficient to achieve useful results, we advise you to start with the easiest method, the Sliders View. Further note that once you use the Sliders or Matrix View, you cannot open your configuration via the Blobs View.",
        "",
        "To confirm your selection, press the 'OK' button.",
        "To discard your selection, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, "Dissimilarity Configuration Method Selection - Help", text)


def menu_help_abstraction(master):
    """help popup for Abstraction Configuration view"""
    text = [
        "The Abstraction Configuration view allows you to configure the abstraction from irrelevant features of the data values based on your domain knowledge. The result of applying the abstraction is a smaller set of shorter values, the abstracted values. This represents a first grouping of the data values, which we call Simple Clustering.",
        "",
        ["Questionnaire"],
        "To achieve an abstraction that fits your data, you should answer the questions based on your domain knowledge. You can start with one of the predefined configurations if you like, but you should carefully read and answer each question since the abstraction has great influence on the final clustering. Note that each question is explained in detail in the corresponding tooltip shown when hovering over the question. Some questions are dynamically enabled/disabled depending on your answers to related questions.",
        "When answering the questions, please use your domain knowledge about the selected data and data field to decide which features of the data values are irrelevant for clustering. You should abstract from features that you expect to find frequently in the data values and that do not alter the values’ meaning significantly.",
        "",
        ["Result Preview"],
        "The result of applying the configured abstraction to the first 100 data values is shown upon clicking the button on the right-hand side. Hence, this is a preview of the Simple Clustering. Each cluster is represented by a yellow block of text showing the contained values. The preview is updated dynamically when you modify your answers.",
        "",
        ["Confirm & Discard"],
        "To confirm your configuration of the abstraction, press the 'OK' button.",
        "To discard your configuration, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, "Abstraction Configuration - Help", text)


def menu_help_data_add(master):
    """help popup for Data Addition view"""
    text = [
        "The Data Addition view allows you to add a data set to the list of supported data sets selectable in the Select Data view. Currently, only XML data is supported. For this, you must specify a name for the data set, which will be displayed in the Select Data view. Further, you must specify the XML file containing the data and specify the data field (i.e. XML element) of interest. Per default, the content of the corresponding XML elements will be extracted. Alternatively, you can specify an attribute whose value will be extracted.",
        "",
        "To confirm your configuration, press the 'OK' button.",
        "To discard your configuration, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, "Data Addition - Help", text)


def menu_help_data_selection(master):
    """help popup for Data Selection view"""
    text = [
        "The Data Selection view allows you to select the data set to be clustered. Each data set consists of a set of data values extracted from a database. When first starting the program, a few predefined data sets are available. To add a data set, press the '+' button below. To remove a data set, press the '-' button below, but be careful as once removed data sets cannot be recovered.",
        "",
        "To confirm your data selection, press the 'OK' button.",
        "To discard your selection, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, "Data Selection - Help", text)


def menu_help_hub(master):
    """help popup for hub view"""
    text = [
        "The Hub view is the central view of this application for data value clustering. It allows you to navigate through the configuration steps and subsequently access the calculated clustering.",
        "",
        ["Configuration"],
        "The data value clustering typically requires you to perform 4 steps: You need to select the data, configure the abstraction for the simple clustering and configure both the dissimilarities and the clustering algorithm for the refined clustering.",
        "The configuration steps are performed in separate views which are opened upon clicking the corresponding button in the hub view. The configuration step required to be performed next is highlighted in blue. For the Dissimilarities and the clustering algorithm, multiple configuration methods are supported. Some methods are designed for beginners, i.e. are easy to use, whereas others are designed for experts and thus allow more flexibility. We advise you to perform the configuration steps from top to bottom, even though in some cases a different order is possible. On the right-hand side, previews of the 4 configurations are shown.",
        "Note that below each configuration button there is a small label indicating the status, i.e. whether no configuration is present, the configuration is in progress, the calculation is in progress or the calculation is done.",
        "",
        ["Execution"],
        "Once configured, the data extraction and abstraction are performed automatically. This typically takes only a few seconds. But since dissimilarity calculation and clustering may take up to multiple hours, they are started manually by pressing the corresponding play button.",
        "",
        ["Results"],
        "Once calculated, you can access the simple and refined clustering via the corresponding buttons. In some cases, simple clustering may be sufficient. Then you do not need to configure the refined clustering. The refined clustering is presented to you together with a questionnaire for evaluating the clustering’s quality. After answering these questions you come back to the hub. Then advice concerning modifications of the configuration based on your answers is shown below the status labels.",
        "",
        ["Managing Configurations & Results"],
        "You can save, load and reset your configuration via the menu at the top of the window. Note that autosave is not supported.",
    ]
    menu_information_display(master, "Hub - Help", text)


def menu_information_display(master, title, content):
    """
    Show window with text
    as help feature for context menu

    :param title: str
        window title
    :param content: list[str]
        help text for window content
        one string per line
    :return:
    """

    root = Toplevel(master)
    # root.geometry("500x200")
    root.title("Help")
    root.configure(bg='white')
    root.resizable(False, True)
    if hasattr(master, "icon"):
        root.icon = master.icon
        root.iconphoto(False, master.icon)

    width = root.winfo_screenwidth() // 2
    Label(root, text=title, font=('TkDefaultFont', 12, 'bold'),
          anchor=W, justify=LEFT, fg="dark green", background='white'
          ).grid(row=1, column=1, sticky=W)

    outer_frame, canvas, scrollable_frame = create_scrollable_frame(root)

    root.rowconfigure(2, weight=1)
    outer_frame.grid(sticky='nswe', row=2, column=1)

    for i, t in enumerate(content):
        if isinstance(t, str):
            l = Label(scrollable_frame, text=t, font=('TkDefaultFont', 10), wraplength=width,
                      anchor=W, justify=LEFT, fg="dark green", background='white')
            l.grid(row=i, column=1, sticky=W + E)
        else:
            l = Label(scrollable_frame, text=t[0], font=('TkDefaultFont', 12, 'bold'),
                  anchor=W, justify=LEFT, fg="dark green", background='white')
            l.grid(row=i, column=1, sticky=W)

    def button_quit():
        root.quit()
        root.destroy()

    button_ok = Button(root, text='OK', command=button_quit, justify=RIGHT, background='snow')
    button_ok.grid(sticky='nwse', row=3, column=1)

    root.update()
    # root.geometry("500x" + str(root.winfo_height() + 10))
    root.protocol("WM_DELETE_WINDOW", button_quit)
    root.mainloop()


if __name__ == "__main__":
    # menu_help_cost_matrix()
    menu_help_blob_input(None)
##########################################################################################
