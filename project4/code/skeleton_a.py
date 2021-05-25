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
    all_flows = wanteutility.get_all_flows(all_paths, demands)

    # Perform max-min fair allocation algorithm
    edges = list(graph.edges)
    print(edges.reverse())

    flow_rate = {}
    print('new prob')

  
    
    while len(all_flows) > 0:
        n = 0
        c = []
        e = 0
        sk = 1000000000000

        for edge in edges:
            c_n = 0
            c_c = []
            edge_l = list(edge)
            for flow in all_flows:
                flow_l = list(flow)
                
                if edge_l[0] in flow_l and edge_l[1] in flow_l and flow_l.index(edge_l[1]) - flow_l.index(edge_l[0]) == 1:
                    c_n+=1
                    c_c.append(flow)
                
            if c_n > 0 and graph.get_edge_data(edge[0],edge[1])['weight']/c_n < sk:
                n = c_n
                e = edge
                c = c_c
                sk = graph.get_edge_data(edge[0],edge[1])['weight']/c_n 
        
        print('n', n, 'c', c, 'e', e)
        print('all flows', all_flows)
        for f in c:
            flow_rate.update({f:sk})
            for i in range(len(f)-1):
                f_l = list(f)
                graph.get_edge_data(f_l[i],f_l[i+1])['weight'] -= sk  
            
        
        edges.remove(e)
        all_flows = [f for f in all_flows if f not in c]

        #print(all_flows)

  
            



    # Finally, write the rates to the output file
    with open(out_rates_filename, "w+") as rate_file:
        for p in all_paths:
            if p in flow_rate.keys():
                s = str("{:10.6f}".format(flow_rate[p]))
                s = s.split()[-1]
                rate_file.write(s+ '\n')
                

            else:
                rate_file.write(str(0) + '\n')


def main():
    for appendix in range(assignment_parameters.num_tests_a):
        solve(
            "../ground_truth/input/a/graph%s.graph" % appendix,
            "../ground_truth/input/a/demand%s.demand" % appendix,
            "../ground_truth/input/a/path%s.path" % appendix,
            "../myself/output/a/rate%s.rate" % appendix
        )


if __name__ == "__main__":
    main()
