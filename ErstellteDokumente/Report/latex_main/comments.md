
------- Comments for the Tex-Files in this folder ----
Use this document to share knowledge / problems / ... ocurring while writing the tex-docs

# Structure of the code:
	- sub-files are stored in the chapter-folder and can be compiled separately from the main document
	- CSV-data will be stored in single sub-folders within the chapter-folders
	- using the subfile-system enables compiling the subfiles and the super-file separately (in \documentclass[../Report.tex]{subfiles} the double-dots are essential)
	- test.tex is used as playground to avoid compiling whole larger documents when just trying a new tex feature, and useable to look code up or to store macros
	- non-implemented content or similar tasks should be described in a short %TODO:
	- structure of labels: type:[chapter].[section].[subsection].name 
		with types: chap (-ter), sec (-tion), subsec (-tion), fig (-ure), eq (-uation, see: eqref), tab (-le), lst (code-snippets), itm (listed item)
	(- if senseful, we should think of adding a sub-section every time we leave open points (or problems) at the end of the concerning section / chapter)
	
# nice to know:
	- reference to pages/points in the doc where no \label is possible by using \phantomsection
	- input csv via \pgfplotstableread makes it necessary to ignore chars with j, (, ) and /.style={string type} s.t. complex values are extracted as strings!
	- use \nameref to reference to the name (not number) of the labelled position
	- possible useful: pkg xr or zref to enable references between different subfiles (haven't successfully handled it)
	