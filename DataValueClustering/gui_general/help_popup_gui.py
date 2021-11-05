'''text popup for context menu, used as help'''
import os
from pathlib import Path
from tkinter import Label, Toplevel, W, LEFT, E, RIGHT, Button, N
from PIL import Image
from PIL.ImageTk import PhotoImage
from math import floor

from gui_general.scrollable_frame import create_scrollable_frame
from gui_general.window_size import set_window_size_simple


def menu_help_hub(master, restricted):
    """help popup for hub view"""
    caption = "Hub"
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
        {"\\hub_execute_dissimilarities" + ("_restricted" if restricted else "") + ".png"},
    ]
    menu_information_display(master, caption, text)


def menu_help_data_selection(master, restricted):
    """help popup for Data Selection view"""
    caption = "Data Selection"

    text = [
        "The Data Selection view allows you to select the data set to be clustered. Each data set consists of a set of data values extracted from a database. When first starting the program, a few predefined data sets are available.",
        "As shown by the screenshot below, we chose the 'classification' data value set for our running example. It contains values of the corresponding LIDO field for classifying the object described by the data.",
        None if restricted else "To add a data set, press the '+' button below. For this, a local BaseX client is required. For this, please install BaseX and execute 'bin/basexserver.bat'.",
        None if restricted else "To remove a data set, press the '-' button below, but be careful as once removed data sets cannot be recovered.",
        "",
        "To confirm your data selection, press the 'OK' button.",
        "To discard your selection, press the 'X' button in the upper right corner.",
        {"\\data_selection" + ("_restricted" if restricted else "") + ".png"},
    ]
    menu_information_display(master, caption, text)


def menu_help_data_add(master):
    """help popup for Data Addition view"""
    caption = "Data Addition"
    text = [
        "The Data Addition view allows you to add a data set to the list of supported data sets selectable in the Select Data view. Currently, only XML data is supported. For this, you must specify a name for the data set, which will be displayed in the Select Data view. Further, you must specify the XML file containing the data and specify the data field (i.e. XML element) of interest. In the example below we chose the field 'lido:extentMeasurements'. Per default, the content of the corresponding XML elements will be extracted. Alternatively, you can specify an attribute whose value will be extracted.",
        "",
        "To confirm your configuration, press the 'OK' button.",
        "To discard your configuration, press the 'X' button in the upper right corner.",
        {"\\data_addition.png"},
    ]
    menu_information_display(master, caption, text)


def menu_help_abstraction(master, restricted):
    """help popup for Abstraction Configuration view"""
    caption = "Abstraction Configuration"
    text = [
        "The Abstraction Configuration view allows you to configure the abstraction from irrelevant features of the data values based on your domain knowledge. The result of applying the abstraction is a smaller set of shorter values, the abstracted values. This represents a first grouping of the data values, which we call Simple Clustering.",
        "",
        ["Questionnaire"],
        "To achieve an abstraction that fits your data, you should answer the questions based on your domain knowledge. You can start with one of the predefined configurations. The default configuration typically yields good results.",
        "Please use your domain knowledge to abstract from features that you expect to find frequently in the data values and that do not alter the values’ meaning significantly.",
        "For our running example we chose the default configuration. Since we expect a variety of textual values, we assume that which concrete letters occur, whether they are capitalized or not and how long the words are does not influence the meaning of the values significantly. Even if unexpected digits occur, the concrete digits and the length of digit sequences is not of interest.",
        "The less questions you answer with 'yes' the loner the runtime of the dissimilarity calculation will be.",
        "Note that each question is explained in detail in the corresponding Tooltip shown when hovering over the question. Some questions are dynamically enabled/disabled depending on your answers to related questions.",
        "",
        ["Result Preview"],
        "The result of applying the configured abstraction to the first 100 data values is shown upon clicking the 'Preview' button on the right-hand side. Hence, this is a preview of the Simple Clustering. Each cluster is represented by a yellow block of text showing the contained values. The preview is updated dynamically when you modify your answers.",
        "As the screenshot below shows, the abstraction of the first 100 data values often does not provide a sufficient overview of the whole abstraction.",
        "",
        ["Confirm & Discard"],
        "To confirm your configuration of the abstraction, press the 'OK' button.",
        "To discard your configuration, press the 'X' button in the upper right corner.",
        {"\\abstraction_normal_tip" + ("_restricted" if restricted else "") + ".png"},
        {"\\abstraction_preview" + ("_restricted" if restricted else "") + ".png"},
    ]
    menu_information_display(master, caption, text)


def menu_help_distance_slider(master, restricted):
    """help popup for Dissimilarity Configuration - Sliders view"""
    caption = "Dissimilarity Configuration - Sliders"
    text = [
        "The Sliders view allows configuring the calculation of Dissimilarities between data values. More precisely, you weight the influence of certain characters or character sequences on the dissimilarity between data values in which they occur. These weights are specified via sliders. You should choose the weights based on your domain knowledge about the data field analysed.",
        "",
        ["Character Groups"],
        "On the left-hand side, the characters (and character sequences) are specified. Depending on the abstraction they are represented as enumerations (if not abstracted), as for example '.,:;!?' in the first screenshot below, or via a descriptive label (if abstracted), as for example '<letter_sequences>'. The Tooltips provide explanations. All characters (and sequences) of the same group are assigned the same weight.",
        "",
        ["Custom Character Groups"],
        "When activating 'Custom Character Groups', another column appears on the left-hand side containing an entry field per group, as shown by the secon screenshot below. This column allows you to modify the groups. Here abstracted features are not represented by the descriptive label but by the single character to which they were abstracted. The meaning of these characters is indicated by the middle column. For example 'b' represents letter sequences. Again, not abstracted features are represented as enumerations. Again, the Tooltips provide explanations.",
        "You can move characters between entry fields to move them between groups. Note that only the first occurrence of a character in one of the groups is relevant. Rows with empty entries are ignored. Characters that are not present in the abstracted data values are ignored. Warnings will be displayed if these cases occur. The last line represents all characters not mentioned in the previous lines.",
        "You can add and remove groups, i.e. lines, via the '+' and '-' buttons.  The default groups are automatically derived from the abstraction configuration and serve as a good starting point. To reset the groups correspondingly, press the 'Reset' button.",
        "As indicated by the screenshots below, in our running example, we moved '-' to a separate group so we could give it a different weight.",
        "",
        ["Weights"],
        "Per group, you can specify the weight via the slider given on the right-hand side. This input method is limited such that you only specify the relative influence of characters (and character sequences) on the dissimilarity between data values. Thus, higher weights for a group mean more dissimilarity caused by the presence of these characters in data values. A weight of zero means these characters do not have any influence on the dissimilarity. You should choose higher weights for characters that you do not expect to find regularly in the data values and for characters that may cause great dissimilarity of the data values.",
        "For our running example on classification values we expect mainly letter sequences and blank spaces, so we set those weights low. Since we do not expect digit sequences (= integers), punctuation marks, and math operators and assume they could have a significant impact on the values' meaning, we chose their weights high. For brackets, quotation marks and minus signs we chose medium weights as we do not really expect many of them but still assume that their influence on the values' meaning is limited.",
        None if restricted else "To specify the weights more flexibly, choose Expert Mode.",
        "",
        ["Confirm & Discard"],
        "To confirm your modifications of the weights, press the 'OK' button.",
        "To discard your modifications, press the 'X' button in the upper right corner.",
        {"\\sliders_normal" + ("_restricted" if restricted else "") + ".png"},
        {"\\sliders_custom" + ("_restricted" if restricted else "") + ".png"},
    ]
    menu_information_display(master, caption, text)


def menu_help_blob_input(master, restricted):
    """help popup for Dissimilarity Configuration - Blobs view"""
    caption = "Dissimilarity Configuration - Blobs"
    text = [
        "The Blob view allows configuring the calculation of Dissimilarities between data values. More precisely, you weight the influence of the insertion, deletion and substitution of certain characters or character sequences on the dissimilarity between data values. This is done by moving and scaling graphical objects on a 2D canvas, which we call blobs. You should choose the weights based on your domain knowledge about the data field analysed.",
        "",
        ["Blobs"],
        "Each of the blobs on the canvas represents a group of characters (or sequences of characters) indicated by the label. The empty blue blob represents an empty text. The groups are automatically derived from your configuration of the abstraction.",
        "",
        ["Distance"],
        "The distances between blobs represent the weights of replacing corresponding characters, i.e. the influence on the dissimilarity of data values caused by such a replacement. The weight of deleting and inserting a character is represented by the distance to the special empty blue blob.",
        # interpretation
        "The dissimilarity between blobs is measured between their centres. When two blobs of size 1 just barely touch each other, the dissimilarity between them is interpreted as the value 1.",
        # controls
        "The distances can be modified via Drag & Drop.",
        "Higher distances, i.e. weights, mean more dissimilarity caused by the deletion, insertion or substitution of corresponding characters. Based on your domain knowledge, you should choose higher weights for the insertion and deletion of characters that you do not expect to find regularly in the data values and for characters that may cause great dissimilarity of the data values. You should choose higher weights for the substitution of characters that are dissimilar in meaning while choosing lower weights for the substitution of rather similar characters.",
        "For our running example on classification values we expect mainly letter sequences and blank spaces, so we positioned them close to the empty blue blob. Since we do not expect digit sequences (= integers), punctuation marks, and math operators and assume they could have a significant impact on the values' meaning, we placed them further away from all other blobs. For brackets, quotation marks and minus signs we placed the blobs in medium range of the blue blob and most other blobs as we do not really expect many of them but still assume that their influence on the values' meaning is limited. "
        "",
        ["Size"],
        "The size of each blob represents the weight of substituting characters of the represented group by each other. Some blobs cannot be scaled. They represent groups of characters, whose concrete manifestation was abstracted from. Their size is fixed to the minimal possible size and they are slightly less saturated. Which blobs are fixed depends on your configuration of the abstraction.",
        # interpretation
        "The minimum size represents the value 0, while the default size is 1.",
        # controls
        "The size of non-fixed blobs can be modified via the mouse wheel while the mouse hovers over the blob. The default size of 1 can be restored by pressing N ('normalize').",
        "",
        ["Confirm, Reset & Discard"],
        "To reset the position of the blobs, press the 'Reset' button.",
        "To specify the weights more flexibly, select 'Expert Mode'.",
        "To confirm your modifications of the weights, press the 'OK' button.",
        "To discard your modifications, press the 'X' button in the upper right corner.",
        {"\\blob_v2" + ("_restricted" if restricted else "") + ".png"},
    ]
    menu_information_display(master, caption, text)


def menu_help_cost_map(master):
    """help popup for Dissimilarity Configuration - Matrix view"""
    caption = "Dissimilarity Configuration - Matrix"
    text = [
        "The Matrix View allows configuring the calculation of Dissimilarities between data values. More precisely, you weight the influence of the insertion, deletion and substitution of certain characters or character sequences on the dissimilarity between data values. These weights are specified entirely flexible via numerical values.",
        "The weights for character deletions are represented by the '<delete>' column. Those for character insertions are represented by the '<insert>' row. The weight for substituting characters of group i by characters of group j (or vice versa) is represented by the cell in row i and column j and by the cell in row j and column i. You should choose the weights based on your domain knowledge about the data field analysed.",
        "",
        ["Character Groups"],
        "The left input fields represent groups of characters. Abstracted features are represented by the single character to which they were abstracted. The meaning of these characters is indicated by the second column. Not abstracted features are represented as enumerations. The Tooltips provide explanations. Note that the interface supports sequences like 'a-z' or 'A-Z' for letters and '0-9' for digits.",
        "You can move characters between entry fields to move them between groups. Note that only the first occurrence of a character in one of the groups is relevant. Rows with empty entries are ignored. Characters that are not present in the abstracted data values are ignored. Warnings will be displayed if these cases occur. The last line represents all characters not mentioned in the previous lines.",
        "You can add and remove groups, i.e. lines, via the '+' and '-' buttons.  The default groups are automatically derived from the abstraction configuration and serve as a good starting point. To reset the groups correspondingly, press the 'Reset' button.",
        "",
        ["Weights"],
        "You must enter the weights of character deletions ('<delete>' column), insertions  ('<insert>' row) and substitutions (rest of the matrix) as numbers. The first column and row represent the empty string, therefore effectively deletions and insertions. Here the weights of deleting and inserting the corresponding character are entered. The weight in row i and column j represents the weight for substituting characters of group i by characters of group j and vice versa. Only the relative size of the weights matters.",
        "The dissimilarity measure between two values shall be symmetrical. That means the dissimilarity from value A to value B is the same as from B to A. Because of this, the matrix is mirrored on the diagonal. The entry fields above the diagonal are read-only.",
        "Higher weights mean more dissimilarity caused by the deletion, insertion or substitution of corresponding characters. Based on your domain knowledge, you should choose higher weights for the insertion and deletion of characters that you do not expect to find regularly in the data values and for characters that may cause great dissimilarity of the data values. You should choose higher weights for the substitution of characters that are dissimilar in meaning while choosing lower weights for the substitution of rather similar characters.",
        "",
        ["Capitalization Change"],
        "The Capitalization Change entry represents a special weight, namely the weight for substituting a lower case letter by its upper case variant, and vice versa.",
        "",
        ["Confirm, Reset & Discard"],
        "To confirm your modifications of the weights, press the 'OK' button.",
        "To reset the whole matrix, press the 'Reset' button.",
        "To discard your modifications, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, caption, text)


def menu_help_clustering_selection(master):
    """help popup for Clustering Algorithm Selection view"""
    caption = "Clustering Algorithm Selection"
    text = [
        "The Algorithm Selection view allows you to choose a clustering algorithm. The Tooltips provide information on the level of difficulty of the algorithm configuration and potential drawbacks of the algorithms. Typically hierarchical clustering achieves good results. That is why this algorithm is used when simple algorithm configuration is selected in Hub.",
        "",
        # ["Questionnaire"],
        # "To have a reference point, which algorithm is the most fitting for your purpose, we offer a short questionnaire on the left-hand side.",
        # "",
        # ["Algorithm Selection"],
        # "Depending on your answers, the list of fitting algorithms shown on the right-hand side is updated dynamically.",
        # "",
        ["Confirm & Discard"],
        "To confirm your selection, press the 'OK' button.",
        "To discard your selection, press the 'X' button in the upper right corner.",
        {"\\algo_selection_expert.png"},
    ]
    menu_information_display(master,  caption, text)


def menu_help_clustering_configuration(master, restricted):
    """help popup for Clustering Parameter Configuration view"""
    caption = "Clustering Parameter Configuration"
    text = [
        "The Clustering Parameter Configuration view allows you to configure the chosen clustering algorithm, thus specifying its parameters.",
        "",
        ["Parameters"],
        "The view lists all parameters that can be specified. A brief explanation of each parameter is given below its title. There are three different input methods for the three types of parameters:",
        " • sliders (for numerical values)",
        " • radio buttons (for enumerations)",
        " • check boxes (for booleans)",
        None if restricted else "The list of parameters is split by the caption 'Expert Parameters'. Parameters above this caption should be considered in any case. The parameters below this caption, however, can be ignored in most cases as the default values are suitable. Modification is only encouraged for users who know the details of the selected clustering algorithm.",
        "",
        ["Assistance"],
        "The values that are selected per default often serve as a good starting point for your first iteration. To reset the parameter value to this default value, press the 'Reset' button. For some parameters, a plot showing extra information is provided when pressing the 'Show plot' button.",
        "For our running example we used the default values.",
        "For hierarchical clustering, the Dendrogram is shown when clicking the 'Show plot' button. As the screenshot below indicates, the x-axis show the distances at which the two closest clusters are merged and the y-axis shows the representative values.",
        "",
        ["Optional Parameters"],
        "Some parameters are optional or only used under specific circumstances. When they are not used, they are greyed out. Optional parameters can be enabled and disabled via a checkbox on the left-hand side.",
        "",
        ["Dependencies"],
        "In some cases, there are dependencies between the parameters. They are ensured automatically. Some dependencies result in the (de-)activation of a parameter or the modification of the range of another parameter.",
        "",
        ["Confirm & Discard"],
        "To confirm your configuration, press the 'OK' button.",
        "To discard your configuration, press the 'X' button in the upper right corner.",
        {"\\param_simple.png"},
        {"\\param_expert_1.png" if not restricted else ""},
        {"\\param_expert_2.png" if not restricted else ""},
    ]
    menu_information_display(master, caption, text)


def menu_help_result(master):
    """help popup for Clustering Result & Evaluation view"""
    caption = "Clustering Result & Evaluation"
    text = [
        "The Clustering Result & Evaluation view provides information on the calculated clustering and supports you in evaluating it.",
        "",
        ["MDS Scatter Plot"],
        "On the left-hand side, below some quantitative meta-information on the calculated clustering, the MDS Scatter Plot is shown. It gives an overview of the clustering. Each dot represents an abstracted data value. The distances between the dots represent the dissimilarities between the abstracted data values. Therefore, the closer the dots are, the more similar the values are. Each cluster is represented by a different colour. This plot allows you to quickly get an overview of the compactness and separation of the clustering.",
        "A clustering is compact if there is a high similarity within clusters and it is separate if there is a low similarity between clusters. In general, a good clustering should have high compactness and separation. If the colours are very mixed, this may hint at the low meaningfulness of the clustering (cf. evaluation question 1). The plot may also assist you in answering evaluation question 2. But make sure to also check the entire clustering provided as an Excel file before answering the questions.",
        "",
        ["Clustering"],
        "Most importantly, you can access the complete clustering provided in an Excel file via the green button on the left-hand side. Upon first opening the file, you must specify the save path.",
        "As shown by the screenshots below, the Excel file contains four sheets, that present the clutering:",
        " • The first one shows the clustering of the original values.",
        " • The second one shows the clustering of the abstracted values employing original values as representatives.",
        " • The third sheet additionally shows the variance within each cluster and the dissimilarity of each value to the others in the same cluster.",
        " • The fourth sheet shows the mapping between original and representative values.",
        "An extremely high variance within a cluster indicates that you should consider analysing this cluster separately (cf. evaluation question 4) as it may be too heterogeneous to oversee the types of contained values. You should further take a look at values with an extremely high dissimilarity to the other values in the same cluster, as they may be significantly different from those.",
        "",
        ["Clustering Evaluation"],
        "After having familiarized yourself with the clustering, you need to evaluate the clustering, i.e. find out whether you are satisfied with the clustering or need another iteration with a modified configuration. The evaluation questionnaire given on the right-hand side supports this process. Please read and answer each question carefully. Note that Tooltips of the answers provide explanations.",
        "After you have answered the questions, advice concerning another iteration is given at the bottom. If we suggest doing another iteration, advice on the modification of the configuration for the next iteration is calculated. After returning to the Hub, this advice is given there and in the configuration views in blue text.",
        "",
        ["Confirm & Discard"],
        "To confirm your evaluation answers, press the 'OK' button.",
        "To discard your evaluation answers, press the 'X' button in the upper right corner.",
        {"\\excel_refined_sheets.png"},
        {"\\excel_refined_original.png"},
        {"\\excel_refined_repr.png"},
        {"\\excel_refined_repr_dist.png"},
        {"\\excel_refined_mapping.png"},

    ]
    menu_information_display(master, caption, text)


def menu_help_distance_choice(master):  # REMOVED
    """help popup for Dissimilarity Configuration Method Selection view"""
    caption = "Dissimilarity Configuration Method Selection"
    text = [
        "The Dissimilarity Configuration Method Selection view allows you to select a method for configuring the dissimilarity calculation, i.e. for weighting the similarity between character groups based on your domain knowledge. Currently, only the weighted Levenshtein distance is supported and can be configured via 3 different methods. The easier methods allow less flexibility. But as in most cases, the easiest method is sufficient to achieve useful results, we advise you to start with the easiest method, the Sliders View. Further note that once you use the Sliders or Matrix View, you cannot open your configuration via the Blobs View.",
        "",
        "To confirm your selection, press the 'OK' button.",
        "To discard your selection, press the 'X' button in the upper right corner.",
    ]
    menu_information_display(master, caption, text)


def menu_information_display(master, caption, content):
    """
    Show window with text
    as help feature for context menu

    :param caption: str
        window caption
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

    Label(root, text=caption, font=('TkDefaultFont', 12, 'bold'),
          anchor=W, justify=LEFT, fg="dark green", background='white'
          ).grid(row=1, column=1, sticky=W)

    outer_frame, canvas, scrollable_frame = create_scrollable_frame(root)
    root.rowconfigure(2, weight=1)
    outer_frame.grid(sticky='nswe', row=2, column=1)

    dir_path = str(Path(__file__).parent.parent) + "\\gui_general\\help_screenshots"
    os.chdir(dir_path)

    for i, t in enumerate(content):
        if isinstance(t, str):
            l = Label(scrollable_frame, text=t, font=('TkDefaultFont', 10), wraplength=width,
                      anchor=W, justify=LEFT, fg="dark green", background='white')
            l.grid(row=i, column=1, sticky=W + E)
        elif isinstance(t, list):
            l = Label(scrollable_frame, text=t[0], font=('TkDefaultFont', 12, 'bold'),
                  anchor=W, justify=LEFT, fg="dark green", background='white')
            l.grid(row=i, column=1, sticky=W)
        elif isinstance(t, set):
            pop = t.pop()
            if pop != "":
                img = Image.open(dir_path + pop)
                if img.width > width:
                    height_new = floor(img.height * width/img.width)
                    img = img.resize((width, height_new), Image.ANTIALIAS)
                img = PhotoImage(img)
                l = Label(scrollable_frame, image=img)
                l.grid(row=i, column=1, sticky=W+E)

    def button_quit():
        root.quit()
        root.destroy()

    button_ok = Button(root, text='OK', command=button_quit, justify=RIGHT, background='snow')
    button_ok.grid(sticky='nwse', row=3, column=1)

    root.update()
    # root.geometry("500x" + str(root.winfo_height() + 10))
    root.protocol("WM_DELETE_WINDOW", button_quit)
    set_window_size_simple(root)

    root.mainloop()


if __name__ == "__main__":
    # menu_help_cost_matrix()
    menu_help_blob_input(None)

