# The MIT License (MIT)
#
# Copyright (c) 2019 Simon Kassing (ETH)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

try:
    from . import wanteutility
except (ImportError, SystemError):
    import wanteutility

try:
    from . import assignment_parameters
except (ImportError, SystemError):
    import assignment_parameters

def solve(in_graph_filename, in_demands_filename, in_paths_filename, out_rates_filename):

    # Read in input
    graph = wanteutility.read_graph(in_graph_filename)
    demands = wanteutility.read_demands(in_demands_filename)
    all_paths = wanteutility.read_all_paths(in_paths_filename)
    paths_x_to_y = wanteutility.get_paths_x_to_y(all_paths, graph)

    path_var = {}
    
    for i in range(len(all_paths)):
        path_var.update({all_paths[i]: 'p_'+str(i)})
        

    # Write the linear program
    with open("../myself/output/b/program.lp", "w+") as program_file:
        
        program_file.write('max: Z ;\n')
        
        #program_file.write('    Z ;\n')
    
        #program_file.write('Subject To ;\n')

        for d in demands:
                d_l = list(d)
                s_to_t_paths = paths_x_to_y[d_l[0]][d_l[1]]
                
                if len(s_to_t_paths) >= 1:
                    program_file.write(path_var.get(s_to_t_paths[0]) )
                for i in range(1,len(s_to_t_paths)):
                    program_file.write(' + ' + path_var.get(s_to_t_paths[i]))
                if len(s_to_t_paths) >= 1:
                    program_file.write(' - Z > 0 ;\n')

        for e in graph.edges:
            s = ''
            eps = []
            for p in all_paths:
                e_l = list(e)
                p_l = list(p)
                if e_l[0] in p_l and e_l[1] in p_l and p_l.index(e_l[1]) - p_l.index(e_l[0]) == 1:
                    eps.append(p)
            if len(eps) > 0:
                s += path_var.get(eps[0]) 
            for i in range(1, len(eps)):
                s += ' + ' + path_var.get(eps[i]) 
            if len(eps) > 0:
                program_file.write( s + ' < ' + str(graph.get_edge_data(e_l[0],e_l[1])['weight']) + ';\n' )

        for p in path_var.keys():  
            program_file.write(path_var.get(p) + ' > 0 ; \n')
        
    # Solve the linear program
    var_val_map = wanteutility.ortools_solve_lp_and_get_var_val_map(
        '../myself/output/b/program.lp'
    )

    # Retrieve the rates from the variable values
    for var in var_val_map:
        print(var,' ', var_val_map.get(var))


    # Finally, write the rates to the output file
    with open(out_rates_filename, "w+") as rate_file:
        for p in path_var.keys():
            p_var = path_var.get(p)
            r = var_val_map.get(p_var)
            rate_file.write(str(r)+'\n')
            


def main():
    for appendix in range(assignment_parameters.num_tests_b):
        solve(
            "../ground_truth/input/b/graph%s.graph" % appendix,
            "../ground_truth/input/b/demand%s.demand" % appendix,
            "../ground_truth/input/b/path%s.path" % appendix,
            "../myself/output/b/rate%s.rate" % appendix
        )


if __name__ == "__main__":
    main()
