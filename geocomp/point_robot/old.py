        '''
        for x in l_node:
            node = self.node_list[x]
            at = self.node_list[x].info
            at.hide()
            self.rmv_trapezoid(at)
            if cnt == 0:
                # QUEBRA O TRAPEZIO EM TRES PEDACOS
                t_left = copy.copy(at)
                t_left.p_right = segment.p_left
                t_left.pid = self.get_trapezoid()
                t_left.blink()

                t_bottom = copy.copy(at)
                t_bottom.s_top = segment
                t_bottom.p_left = segment.p_left
                t_bottom.pid = self.get_trapezoid()
                t_bottom.blink()

                t_top = copy.copy(at)
                t_top.s_bottom = segment
                t_top.p_left = segment.p_left
                t_top.pid = self.get_trapezoid()
                t_top.blink()

                if at.t_upper_left != None:
                    at.t_upper_left.t_upper_right = t_left
                    at.t_upper_left.t_lower_right = t_left                   

                if at.t_lower_left != None:
                    at.t_lower_left.t_upper_right = t_left
                    at.t_lower_left.t_lower_right = t_left

               
                self.trapezoid_list[t_left.pid] = t_left
                self.trapezoid_list[t_bottom.pid] = t_bottom
                self.trapezoid_list[t_top.pid] = t_top     

                lu_id = t_top.pid 
                ll_id = t_bottom.pid

                a = SNode(None, None, 0, t_left)
                b = SNode(None, None, 0, t_top)
                c = SNode(None, None, 0, t_bottom) 
                id_a = self.add_node(a)
                id_b = self.add_node(b)
                id_c = self.add_node(c)     
                s = SNode(id_b, id_c, 1, segment);
                id_s = self.add_node(s)
                p = SNode(id_a, id_s, 2, segment.p_left)
                self.node_list[node.pid] = p

            elif cnt == tot - 1:
                # QUEBRA O TRAPEZIO EM TRES PEDACOS
                t_right = copy.copy(at)
                t_right.p_left = segment.p_right
                t_right.pid = self.get_trapezoid()
                t_right.blink()

                t_bottom = copy.copy(at)
                t_bottom.s_top = segment
                t_bottom.p_right = segment.p_right
                t_bottom.pid = self.get_trapezoid()
                t_bottom.blink()


                t_top = copy.copy(at)
                t_top.s_bottom = segment
                t_top.p_right = segment.p_right
                t_top.pid = self.get_trapezoid()
                t_top.blink()

                self.trapezoid_list[lu_id].t_upper_right = t_top
                self.trapezoid_list[lu_id].t_lower_right = t_top
                self.trapezoid_list[ll_id].t_upper_right = t_bottom
                self.trapezoid_list[ll_id].t_lower_right = t_bottom

                if at.t_upper_right != None:
                    at.t_upper_right.t_upper_left = t_right
                    at.t_upper_right.t_lower_left = t_right                  

                if at.t_lower_right != None:
                    at.t_lower_right.t_upper_left = t_right                      
                    at.t_lower_right.t_lower_left = t_right

                self.trapezoid_list[t_right.pid] = t_right
                self.trapezoid_list[t_bottom.pid] = t_bottom
                self.trapezoid_list[t_top.pid] = t_top     
               
                a = SNode(None, None, 0, t_right)
                b = SNode(None, None, 0, t_top)
                c = SNode(None, None, 0, t_bottom) 
                id_a = self.add_node(a)
                id_b = self.add_node(b)
                id_c = self.add_node(c)
                s = SNode(id_b, id_c, 1, segment);
                id_s = self.add_node(s)
                q = SNode(id_s, id_a, 2, segment.p_right)
                id_q = self.add_node(q)
                self.node_list[node.pid] = q

            else:
                # QUEBRA O TRAPEZIO EM DOIS PEDACOS
                t_bottom = copy.copy(at)
                t_bottom.s_top = segment
                t_bottom.pid = self.get_trapezoid()
                t_bottom.blink()

                t_top = copy.copy(at)
                t_top.s_bottom = segment
                t_top.pid = self.get_trapezoid()
                t_top.blink()

                self.trapezoid_list[lu_id].t_upper_right = t_top
                self.trapezoid_list[lu_id].t_lower_right = t_top
                self.trapezoid_list[ll_id].t_upper_right = t_bottom
                self.trapezoid_list[ll_id].t_lower_right = t_bottom

                lu_id = t_top.pid 
                ll_id = t_bottom.pid
 

                self.trapezoid_list[t_bottom.pid] = t_bottom
                self.trapezoid_list[t_top.pid] = t_top     

                a = SNode(None, None, 0, t_top)
                b = SNode(None, None, 0, t_bottom) 
                id_a = self.add_node(a)
                id_b = self.add_node(b)
                s = SNode(id_a, id_b, 1, segment);
                id_s = self.add_node(s)
                self.node_list[node.pid] = s


            cnt = cnt + 1

        '''
