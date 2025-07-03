from control_flow_graph import ControlFlowGraph

def create_cfg() -> ControlFlowGraph:
    """
       Create the CFG from the paper example:
       0. gcd(int m, int n) {
       1. if (n > m) {
       2.   r = m;
       3.   m = n;
       4.   n = r;
       5.   r = m % n;
       6.   while (r != 0) {
       7.     m = n;
       8.     n = r;
       9.     r = m % n;
       10.  }
       11.  return n;
       12. }
       """
    cfg = ControlFlowGraph()

    cfg.add_edge(0, 1, 'branch')  # if statement
    cfg.add_edge(0, 12, 'branch')  # else branch (direct to end)

    cfg.add_edge(1, 2, 'sequential')
    cfg.add_edge(2, 3, 'sequential')
    cfg.add_edge(3, 4, 'sequential')
    cfg.add_edge(4, 5, 'sequential')
    cfg.add_edge(5, 6, 'sequential')

    cfg.add_edge(6, 7, 'loop')  # loop body
    cfg.add_edge(7, 8, 'sequential')
    cfg.add_edge(8, 9, 'sequential')
    cfg.add_edge(9, 6, 'loop')  # back to loop condition

    cfg.add_edge(6, 10, 'branch')  # loop exit
    cfg.add_edge(10, 11, 'sequential')
    cfg.add_edge(11, 12, 'sequential')

    cfg.assign_weights()

    return cfg