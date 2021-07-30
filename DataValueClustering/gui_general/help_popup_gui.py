'''text popup for context menu, used as help'''
from tkinter import *


def menu_help_result(master):
    """help popup for Result view"""
    text = [
        "The Result view provides information on the calculated clustering and supports you in validating it.",
        "",
        ["Meta-Information"],
        "In the top left, quantitative meta-information on the calculated clustering are given.",
        "Below, the MDS Scatter Plot gives an overview of the clustering.",
        "Each dot represents an abstracted data value.",
        "The distances between the blobs represent the distances, i.e. dissimilarities, between the abstracted data "
        "values.",
        "Each cluster is represented by a different color.",
        "Noise is colored black.",
        "This plot allows you to quickly get an overview of the compactness and separation of the clustering.",
        "A clustering is compact if there is a high similarity within clusters and it is separate if there is a low ",
        "similarity between clusters.",
        "In general, a good clustering should have high compactness and separation.",
        "If the colors are very mixed, this may hint at low meaningfulness of the clustering (cf. validation question 1).",
        "The plot may also assist you in answering validation question 2.",
        "But make sure to also check the entire clustering provided as an Excel file before answering the questions.",
        "",
        ["Clustering"],
        "Most importantly, you can access the complete clustering provided in an Excel file via the green button below.",
        "For this, you must specify the save path first.",
        "The Excel file contains three sheets.",
        "The first one shows the clustering of the original values.",
        "The second one shows the clustering of the abstracted values by means of original values as representatives.",
        "The third sheet additionally shows the variance within each cluster and the distance of each value to the ",
        "others in the same cluster.",
        "An extremely high variance within a cluster indicates that you should consider analysing this cluster ",
        "separately (cf. validation question 4) as it may be too heterogeneous to oversee the types of contained values.",
        "You should further take a look at values with an extremely high distance to the other values in the ",
        "same cluster, as it may be significantly different from those.",
        "",
        ["Validation"],
        "After having familiarized yourself with the clustering, you should validate the clustering, i.e. find out ",
        "whether you are satisfied with the clustering or need another iteration with a modified configuration.",
        "The validation questionnaire given on the right-hand side, supports this process.",
        "In case you are not satisfied with the clustering, we calculate suggestions for modifications of the ",
        "configuration of the next iteration.",
        "The suggestions are given in the configuration views in blue text.",
        "",
        ["Confirm & Discard"],
        "To confirm your validation answers, press the 'OK' button.",
        "To discard your validation answers, press the 'x' button in the upper right corner.",
    ]
    menu_information_display(master, "Result - Help", text)


def menu_help_clustering_configuration(master):
    """help popup for Clustering Configuration view"""
    text = [
        "The Clustering Configuration Selection view allows you to specify the parameter values for the chosen clustering ",
        "algorithm.",
        "",
        ["Parameters"],
        "All parameters that can be specified are listed and brief explanations are given below the title.",
        "You can specify the parameter values via sliders, radio buttons or check boxes depending on the parameter type.",
        "The checkboxes on the left-hand side indicate which parameters are enabled and which are disabled.",
        "In some cases, there are dependencies between the values or activation of multiple parameters. They are ensured ",
        "automatically.",
        "For some parameters, a plot showing fitting information is provided when pressing the 'Show plot' button.",
        "",
        ["Default Values & Recommendations"],
        "The values that are specified per default can serve as a good starting point for your first iteration.",
        "To reset the parameter value to the default value, press the 'Reset' button.",
        "For enumerations, recommended options are highlighted in light green, while options that are rather not ",
        "recommended are highlighted in light red.",
        "",
        ["Confirm & Discard"],
        "To confirm your configuration, press the 'OK' button.",
        "To discard your configuration, press the 'x' button in the upper right corner.",
    ]
    menu_information_display(master, "Clustering Configuration - Help", text)


def menu_help_clustering_selection(master):
    """help popup for Clustering Algorithm Selection view"""
    text = [
        "The Clustering Algorithm Selection view allows you to choose a clustering algorithm.",
        "",
        ["Questionnaire"],
        "For this, you should answer the questions on the left-hand side.",
        "",
        ["Algorithm Selection"],
        "Depending on your answers, the list of fitting algorithms shown on the right-hand side is updated dynamically.",
        ["Confirm & Discard"],
        "To confirm your selection, press the 'OK' button.",
        "To discard your selection, press the 'x' button in the upper right corner.",
    ]
    menu_information_display(master, "Clustering Algorithm Selection - Help", text)


def menu_help_distance_slider(master):
    """help popup for Slider Input view"""
    text = [
        "The Slider Input view allows you to configure the weights used in the distance calculation via sliders.",
        "",
        ["Character Groups"],
        "On the left-hand side the character groups are specified via enumerations of characters.",
        "Only the first occurrence of a character in one of the groups is relevant.",
        "The last line represents all characters not mentioned in the previous lines.",
        "",
        "Note that some characters actually represent features that were removed by the abstraction.",
        "For example, depending on the abstraction configuration, '1' may represent any integer.",
        "This mapping between characters and the represented features that were abstracted is provided in the column ",
        "'Abstraction Mapping'.",
        "",
        "You are free to modify the character groups.",
        "You can add and remove groups, i.e. lines via the '+' and '-' buttons.",
        "The default groups are automatically derived from the abstraction configuration.",
        "To reset the groups correspondingly, press the 'Reset' button.",
        "",
        ["Weights"],
        "Per character group you specify the weight via the slider given on the right-hand side.",
        "This input method is limited, such that you only specify the relative importance of certain character groups ",
        "concerning the dissimilarity between data values.",
        "Thus, heigher weights for a character group mean more dissimilarity caused by the presence of these characters ",
        "in data values.",
        "You should choose heigher weights for characters that you do not expect to find regularly in the data values ",
        "and for characters that may cause great dissimilarity of the data values.",
        "",
        ["Confirm & Discard"],
        "To confirm your modifications of the weights, press the 'OK' button.",
        "To discard your modifications, press the 'x' button in the upper right corner.",
    ]
    menu_information_display(master, "Slider Input - Help", text)



def menu_help_distance_choice(master):
    """help popup for Distance Choice view"""
    text = [
        "The Distance Choice view allows you to select a method for configuring the distance calculation, i.e. for ",
        "specifying the similarity between character groups.",
        "Currently only the weighted Levenshtein distance is supported and can be configured via 3 different methods.",
        "Note that the easier methods allow less flexibility.",
        "Further note that once you use the Slider or Matrix View, you cannot open your configuration via the Blob View.",
        "",
        "To confirm your selection, press the 'OK' button.",
        "To discard your selection, press the 'x' button in the upper right corner.",
    ]
    menu_information_display(master, "Distance Choice - Help", text)


def menu_help_abstraction(master):
    """help popup for Abstraction Configuration view"""
    text = [
        "The Abstraction Configuration view allows you to configure the abstraction from irrelevant features of the data ",
        "values.",
        "",
        ["Questionnaire"],
        "For this, you should answer the questions on the left-hand side.",
        "You can start with one of the predefined configurations if you like.",
        "When answering the questions, please use your domain knowledge about the selected data and data field to decide ",
        "which feature of the data values are irrelevant for clustering.",
        "Make sure that you do not abstract from features that you do not expect or that may alter the data values’ ",
        "meaning significantly.",
        "Note that each question is explained in detail in the corresponding tool tip shown when hovering over the ",
        "question.",
        "",
        ["Result Preview"],
        "On the right hand side, the result of applying the abstraction to the first 100 data values is shown and ",
        "updated dynamically.",
        "",
        ["Confirm & Discard"],
        "To confirm your configuration of the abstraction, press the 'OK' button.",
        "To discard your configuration, press the 'x' button in the upper right corner.",
    ]
    menu_information_display(master, "Abstraction Configuration - Help", text)


def menu_help_data_add(master):
    """help popup for Add Data view"""
    text = [
        "The Add Data view allows you to add a data set to the list of supported data sets selectable in the Select ",
        "Data view.",
        "Currently only XML data is supported.",
        "For this, you must specify a name for the data set, which will be displayed in the Select Data view.",
        "Further, you must specify the XML file containing the data and specify the data field (i.e. XML element) ",
        "of interest.",
        "Per default the content of the corresponding XML elements will be extracted.",
        "Alternatively you can specify an attribute whose value will be extracted.",
        "",
        "To confirm your configuration, press the 'OK' button.",
        "To discard your configuration, press the 'x' button in the upper right corner.",
    ]
    menu_information_display(master, "Add Data - Help", text)


def menu_help_data_selection(master):
    """help popup for Select Data view"""
    text = [
        "The Select Data view allows you to select the data set to be clustered.",
        "Each data set consists of a set of data values extracted from a database.",
        "When first starting the program, a few predefined data sets are available.",
        "To add a data set, press the '+' button below.",
        "To remove a data set, press the '-' button below, but be careful as once removed data sets cannot be recovered.",
        "",
        "To confirm your data selection, press the 'OK' button.",
        "To discard your selection, press the 'x' button in the upper right corner.",
    ]
    menu_information_display(master, "Select Data - Help", text)


def menu_help_hub(master):
    """help popup for hub view"""
    text = [
        "The Hub view is the central view of this program for data value clustering.",
        "The data value clustering requires you to perform 4 configuration steps: data, abstraction, distance and ",
        "clustering configuration.",
        "The hub view allows you to navigate through the 4 configuration steps and access the calculated clustering ",
        "subsequently.",
        "",
        ["Configuration"],
        "The configuration steps are performed in separate views which are opened upon clicking the corresponding button ",
        "in the hub view.",
        "The configuration step required to be performed next is highlighted in blue.",
        "We advice you to perform the configuration steps in the given order, even though in some cases a different ",
        "order is possible.",
        "On the right hand side you see previews of the 4 configurations.",
        "",
        ["Execution"],
        "Once configured, the data extraction and abstraction are performed automatically.",
        "This typically takes only a few seconds.",
        "But since distance calculation and clustering may take up to multiple hours, they are startet manually by ",
        "pressing the corresponding play button.",
        "Note that below each configuration button there is a small label indicating the status, ",
        "i.e. whether no configuration is present, the configuration is in progress, ",
        "the calculation is in progress or the calculation is done.",
        "",
        ["Managing Configurations & Results"],
        "You can save, load and reset your configuration via the menu.",
        "Once the clustering is ready, you can open the result view to see further information and perform the ",
        "validation or save the clustering in an Excel file.",
    ]
    menu_information_display(master, "Hub - Help", text)


def menu_help_cost_map(master):
    """help popup for matrix view"""
    text = [
        "This view is designed to give full control over the weights used for the calculation of distances between ",
        "data values.",
        "",
        ["Character Groups"],
        "The left input fields represent groups of characters. Please enumerate all characters, that",
        "should be in the group. Note, that the interface supports sequences like 'a-z' or 'A-Z' for",
        "letters and '1-2' for digits.",
        "Only the first occurrence of a character in one of the groups is relevant.",
        "The last row and column represents all characters not mentioned in the lines above.",
        "",
        "Note that some characters actually represent features that were removed by the abstraction.",
        "For example, depending on the abstraction configuration, '1' may represent any integer.",
        "This mapping between characters and the represented features that were abstracted is provided in the second ",
        "column.",
        "",
        "You are free to modify the character groups.",
        "You can add and remove groups, i.e. lines via the '+' and '-' buttons.",
        "The default groups are automatically derived from the abstraction configuration.",
        "To reset the groups correspongingly, press the 'Reset' button.",
        "",
        ["Weights"],
        "You must enter the weights of character deletions (first column), insertions (first row) and substitution ",
        "(rest of the matrix) as numbers.",
        "The first column and row represent the empty string. Here the weights of deleting",
        "and inserting the corresponding character is entered.",
        "The weight in row i and column j represents the weight for substituting the characters represented by row i by ",
        "characters represented by column j.",
        "Only the relative size of the weights matters.",
        "Because the distance between two data values shall be symmetrical, the matrix is",
        "mirrored on the diagonal. The entry fields above the diagonal are read only.",
        "Heigher weights for a character group mean more dissimilarity caused by the deletion/insertion/substitution of ",
        "these characters.",
        "You should choose heigher weights for characters that you do not expect to find regularly in the data values ",
        "and for characters that may cause great dissimilarity of the data values.",
        "",
        ["Confirm, Reset & Discard"],
        "To confirm your modifications of the weights, press the 'OK' button.",
        "To reset character groups, press the 'Reset' button.",
        "To discard your modifications, press the 'x' button in the upper right corner.",
    ]
    menu_information_display(master, "Costmatrix - Help", text)


def menu_help_blob_input(master):
    """help popup for Blob view"""
    text = [
        "This view allows the configuration of the weights used for the calculation of distances between data values by "
        "moving and scaling graphical objects on a 2D canvas.",
        "",
        ["Blobs"],
        "Each of the spheres (we call them 'blobs') in this diagram represent a group of similar",
        "characters. This group of characters is described in the label. There is one empty",
        "blue blob. This represents an empty text.",
        "The character groups are automatically derived from your configuration of the abstraction.",
        "",
        ["Distance"],
        "The distances between blobs represent the weight of replacing corresponding characters. The weight ",
        "of deleting and inserting a character is represented by the distance to the special empty ",
        "blue blob.",
        # interpretation
        "When the blobs just barely touch each other, the distance between them is interpreted",
        "as the value 1.",
        # controls
        "The distances can be modified via Drag & Drop.",
        "",
        "Heigher weights for a character group mean more dissimilarity caused by the deletion/insertion/substitution of "
        "these characters.",
        "You should choose heigher weights for characters that you do not expect to find regularly in the data values "
        "and for characters that may cause great dissimilarity of the data values.",
        "",
        ["Size"],
        "The size of each blob represents the weight of substituting characters of the represented group by each other.",
        "Some blobs cannot be scaled. These are on default fixed on the minimal size and",
        "are slightly less saturated. The fixed blobs depend on your configuration of the abstraction.",
        # interpretation
        "The minimum size represents the value 0. The default size is 1.",
        # controls
        "The size of not fixed blobs can be changed via the scroll wheel while the mouse hovers ",
        "over the blob. The default size can be restored by pressing N on mouse over.",
        "",
        ["Confirm, Reset & Discard"],
        "To confirm your modifications of the weights, press the 'OK' button.",
        "To reset the position of the blobs, press the 'Reset' button.",
        "To discard your modifications, press the 'x' button in the upper right corner.",
    ]
    menu_information_display(master, "Distance Specification - Help", text)


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
    root.resizable(False, False)
    Label(root, text=title, font='Arial 14 bold underline',
          anchor=W, justify=LEFT, fg="green", background='white'
          ).grid(row=1, column=1, sticky=W)

    for i, t in enumerate(content):
        if isinstance(t, str):
            Label(root, text=t, font='Arial 10',
                  anchor=W, justify=LEFT, fg="green", background='white'
                  ).grid(row=i + 2, column=1, sticky=W + E)
        else:
            Label(root, text=t[0], font='Arial 12 bold',
                  anchor=W, justify=LEFT, fg="green", background='white'
                  ).grid(row=i + 2, column=1, sticky=W)

    def button_quit():
        root.quit()
        root.destroy()

    Button(root, text='OK', command=button_quit,
           justify=RIGHT, width=15, background='snow'
           ).grid(row=len(content) + 3, column=1)

    root.update()
    # root.geometry("500x" + str(root.winfo_height() + 10))
    root.protocol("WM_DELETE_WINDOW", button_quit)
    root.mainloop()


if __name__ == "__main__":
    # menu_help_cost_matrix()
    menu_help_blob_input()
