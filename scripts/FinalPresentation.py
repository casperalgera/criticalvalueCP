from manim import * 
from manim_slides import Slide
import csv
from collections import deque


class CVpres(Slide):

    def memoryless(self):
        LAMBDA = 0.5
        S_VAL = 2.0
        T_VAL = 3.0
        COL_LIGHT = ManimColor("#F8F8F8")
        
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 0.6, 0.1],
            x_length=8.5,
            y_length=4.0,
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": np.arange(0, 11, 2)},
        ).to_edge(DOWN, buff=0.75)
        title = Tex("Next we will look at the contact process, but first..", font_size=36, color=COL_LIGHT)
        title.next_to(ax, UP, buff=0.3)
        self.play(Write(title, run_time=0.5))
        self.next_slide()

        title1 = Tex("Let us take a look at the exponential distribution.", font_size=36, color=COL_LIGHT)
        title1.next_to(ax, UP, buff=0.3)

        pdf_graph = ax.plot(lambda x: LAMBDA * np.exp(-LAMBDA * x), x_range=[0, 10], color=COL_LIGHT)
        pdf_label = MathTex(r"f(x)\!=\!\lambda e^{-\lambda x}", font_size=30, color=COL_LIGHT)
        pdf_label.next_to(ax.c2p(1.5, pdf_graph.underlying_function(1.5)), direction=UP, buff=0.2).shift(RIGHT)
        
        self.play(Transform(title, title1, run_time=1), Create(ax, run_time=1), Create(pdf_graph, run_time=1), Write(pdf_label, run_time=1))
        
        self.next_slide()

        prob_t_text = Tex(r"First, let's visualize $P(X > t)$", font_size=36, color=COL_LIGHT).move_to(title)
        self.play(Transform(title, prob_t_text, run_time=1))

        t_marker = Dot(ax.c2p(T_VAL, 0), color=YELLOW)
        t_label = MathTex("t", color=COL_LIGHT).next_to(t_marker, DOWN * 1.8)
        area_t = ax.get_area(pdf_graph, x_range=(T_VAL, 10), color=GREEN, opacity=0.7)
        area_t_label = MathTex("P(X > t)", font_size=30, color=COL_LIGHT).move_to(ax.c2p(T_VAL + 2.5, 0.12))

        self.play(Create(t_marker, run_time=0.5), Write(t_label, run_time=0.5))
        self.play(FadeIn(area_t, run_time=0.5), Write(area_t_label, run_time=0.5))
        
        self.next_slide()

        self.play(FadeOut(area_t, area_t_label, t_marker, t_label, run_time=0.5))
        condition_text = Tex("Given that we've already waited until time $s$...", font_size=36, color=COL_LIGHT).move_to(title)
        self.play(Transform(title, condition_text, run_time=1))
        
        s_marker = Dot(ax.c2p(S_VAL, 0), color=ORANGE)
        s_label = MathTex("s", color=COL_LIGHT).next_to(s_marker, DOWN * 1.8)
        area_s = ax.get_area(pdf_graph, x_range=(S_VAL, 10), color=ORANGE, opacity=0.5)
        area_s_label = MathTex("P(X > s)", font_size=30, color=COL_LIGHT).move_to(ax.c2p(S_VAL + 2, 0.2))

        self.play(Create(s_marker, run_time=0.5), Write(s_label, run_time=0.5))
        self.play(FadeIn(area_s, run_time=0.5), Write(area_s_label, run_time=0.5))

        self.next_slide()

        question_text = Tex("We will determine the probability we need to wait another $t$ seconds.", font_size=36, color=COL_LIGHT).move_to(title)
        self.play(Transform(title, question_text, run_time=1), FadeOut(area_s_label, run_time=0.5))

        st_marker = Dot(ax.c2p(S_VAL + T_VAL, 0), color=RED)
        st_label = MathTex("s+t", color=COL_LIGHT).next_to(st_marker, DOWN*1.8)
        area_st_cond = ax.get_area(pdf_graph, x_range=(S_VAL + T_VAL, 10), color=RED, opacity=0.8)
        area_st_cond_label = MathTex(r"P(X > s+t)", font_size=30, color=COL_LIGHT).move_to(ax.c2p(S_VAL + T_VAL + 1.5, 0.1))
        
        self.play(Create(st_marker, run_time=0.5), Write(st_label, run_time=0.5))
        self.play(FadeIn(area_st_cond, run_time=0.5), Write(area_st_cond_label, run_time=0.5))
        
        self.next_slide()

        self.play(FadeOut(area_s, run_time=0.5))
        shift_text = Tex("Step 1: Shift the distribution to a new origin", font_size=36, color=COL_LIGHT).move_to(title)
        self.play(Transform(title, shift_text, run_time=1), FadeOut(area_st_cond_label, run_time=0.5))
        
        tail_graph_copy = pdf_graph.copy().set_color(YELLOW)
        area_st_cond_copy = area_st_cond.copy()
        
        shift_distance = ax.x_axis.n2p(S_VAL)[0] - ax.x_axis.n2p(0)[0]
        shift_vector = LEFT * shift_distance

        group_to_shift = VGroup(tail_graph_copy, area_st_cond_copy, s_marker, s_label, st_marker, st_label)
        self.play(group_to_shift.animate.shift(shift_vector), run_time=1.5)

        self.play(FadeOut(s_marker, s_label, st_marker, st_label), run_time=0.5)
        
        self.next_slide()

        rescale_title = Tex("Step 2: Rescale the curve so the total area equals 1", font_size=36, color=COL_LIGHT).move_to(title)
        self.play(Transform(title, rescale_title, run_time=1))

        target_graph = ax.plot(lambda x: LAMBDA * np.exp(-LAMBDA * x), x_range=[0, 10-S_VAL], color=YELLOW)
        target_area = ax.get_area(target_graph, x_range=[T_VAL, 10-S_VAL], color=RED, opacity=0.8)
        area_st_cond_label = MathTex(r"P(X > s+t \mid X>s)", font_size=30, color=COL_LIGHT).move_to(ax.c2p(S_VAL + 2, 0.1)).shift(RIGHT * 1.5)
        self.play(
            Transform(tail_graph_copy, target_graph, run_time=1.5),
            Transform(area_st_cond_copy, target_area, run_time=1.5),
            Write(area_st_cond_label, run_time=0.5)
        )
        self.next_slide()

        conclusion_text = Tex("The rescaled distribution is identical to the original!", font_size=36, color=COL_LIGHT).move_to(title)
        self.play(Transform(title, conclusion_text, run_time=1))

        self.play(
            FadeIn(area_t.copy().set_opacity(0.5)),
            FadeIn(t_marker.copy(), t_label.copy()),
            run_time=1
        )
        self.play(Flash(tail_graph_copy, color=GREEN, flash_radius=1.5, run_time=1.5))
        self.wait(1)
        self.next_slide()
        
        final_formula = MathTex(r"P(X > s+t \mid X > s)", r"=", r"P(X > t)", color=COL_LIGHT).scale(1.1).move_to(title)
        
        self.play(
            FadeOut(title, pdf_label, tail_graph_copy, t_marker, t_label, area_st_cond_label, run_time=0.5),
            run_time=0.5
        )
        self.play(
            Transform(area_st_cond_copy, final_formula[0], run_time=1.5),
            Transform(area_t, final_formula[2], run_time=1.5)
        )
        self.play(Write(final_formula[1], run_time=0.5))
    def cpsimulation(self, man, rate):
        path = f'C:\\Users\\caspe\\OneDrive\\Documents\\Universiteit\\Scriptie\\Python\\Visualisations\\Eindpresentatie\\media\\infection_data_rate{rate}.csv'

        men = Group()
        for i in range(-5, 7):
            copy = man.copy().set_color(RED)
            copy.move_to(man.get_center() + 1.2*(i - 0.5) * RIGHT) 
            men.add(copy)
        self.add(*men)

        # Read the CSV file and animate
        with open(path, newline='') as csvfile:
            reader = ([int(cell) for cell in row] for row in csv.reader(csvfile))
            rows = list(reader)

            for i in range(1, len(rows)):
                animations = []
                for j in range(1, len(rows[i])):
                    if rows[i][j] == 1 and rows[i-1][j] == 0:
                        animations.append(men[j-1].animate.set_color(RED))
                    elif rows[i][j] == 0 and rows[i-1][j] == 1:
                        animations.append(men[j-1].animate.set_color(ManimColor("#F8F8F8")))
                if animations:
                    self.play(*animations, run_time=0.1)
        return men
    
    def init_slides(self, slide_title_text):
        old_slide_title = self.canvas.get("title", None)
        new_slide_title = Text(slide_title_text, color=ManimColor("#13242A")).to_corner(UL)
        self.play(FadeOut(old_slide_title), FadeIn(new_slide_title), run_time=0.2)
        self.add_to_canvas(title=new_slide_title)

    def construct(self):
        COL_DARK = ManimColor("#13242A")
        COL_LIGHT = ManimColor("#F8F8F8")
        self.camera.background_color = COL_DARK
        learn_more_text = (  VGroup(
                            Text("The Critical Value of the Contact Process", color=COL_LIGHT),
                            Text("Casper Algera", color=YELLOW),
                            ).arrange(DOWN).scale(0.75))
        self.play(GrowFromCenter(learn_more_text))
        self.next_slide()  

        man = ImageMobject(r'C:\Users\caspe\OneDrive\Documents\Universiteit\Scriptie\Python\Visualisations\Eindpresentatie\media\images\Eindpresentatie\Stickman.png').scale(0.5)

        dot = Dot().scale(0)
        self.play(Transform(learn_more_text, dot))

        top_bar = Rectangle(
            width=config["frame_width"],
            height=1.5,
            fill_color=COL_LIGHT,
            fill_opacity=1,
            stroke_width=0
        ).to_edge(UP, buff=0)
        slide_title = Text("Introduction", color=COL_DARK).to_corner(UL)
        self.add_to_canvas(bar=top_bar, title=slide_title)
        self.play(FadeIn(top_bar), FadeIn(slide_title), run_time = 0.5)


        self.play(FadeIn(man))

        self.next_slide()  

        red_man = man.copy().set_color(RED)
        self.play(Transform(man, red_man), run_time = 0.1)
        self.next_slide()
        men = Group()
        red_man = man.copy().set_color(RED)
        men.add(red_man)
        animations = []
        for dir in [RIGHT, LEFT]:
            copy = man.copy().set_color(COL_LIGHT) 
            copy.move_to(man.get_center())
            men.add(copy)
            animations.append(copy.animate.move_to(man.get_center() + 2 * dir))
        self.add(red_man)
        for m in men[1:]:
            self.add(m) 
        self.play(*animations)
        self.next_slide()

        self.init_slides("Contact process")

        spreadquestion = Text("How does this infection spread?", color=YELLOW).scale(0.75)
        spreadquestion.to_edge(UP).shift(2 * DOWN)
        self.play(GrowFromCenter(spreadquestion))
        self.next_slide()

        explaintext = Tex("$\cdot$ Infected sites heal randomly, on average once per second.", color=COL_LIGHT).scale(0.7).align_on_border(LEFT, buff=0.5)
        explaintext.to_edge(UP).shift(5 * DOWN)
        self.play(Write(explaintext), run_time=0.5)
        self.next_slide()
        explaintext2 = Tex(r"$\cdot$ Infected sites infect their neighbours randomly, on average $\lambda$ times per second.", color=COL_LIGHT).scale(0.7).next_to(explaintext, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(Write(explaintext2), run_time=0.5)
        self.next_slide()
        explaintext3 = Tex(r"$\cdot$ Later more detail, first we will see what it looks like.", color=COL_LIGHT).scale(0.7).next_to(explaintext2, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(Write(explaintext3), run_time=0.5)
        self.next_slide()

        self.wipe(self.mobjects_without_canvas, [])
        self.init_slides("Supercritical")
        men = Group()
        for i in range(-5, 7):
            copy = man.copy().set_color(RED)
            copy.move_to(man.get_center() + 1.2*(i - 0.5) * RIGHT) 
            men.add(copy)

        question_text = Text(f"Infection rate 2", color=ManimColor("#F8F8F8")).scale(0.75)
        question_text.to_edge(UP).shift(2 * DOWN)
        self.play(FadeIn(men), FadeIn(question_text), run_time=0.5)
        
        self.next_slide(loop=True)
        self.remove(*men)   
        men = self.cpsimulation(man, 2)
        self.next_slide(loop=False)


        self.wipe(self.mobjects_without_canvas, [])
        self.init_slides("Subcritical")
        question_text = Text(f"Infection rate 1", color=ManimColor("#F8F8F8")).scale(0.75).to_edge(UP).shift(2 * DOWN)
        self.play(FadeIn(men), FadeIn(question_text), run_time=0.5)
        self.next_slide(loop=False)
        self.remove(men)

        men = self.cpsimulation(man, 1)
        self.next_slide()


        self.init_slides("Critical value")
        vertices = [m.get_center() for m in men]
        
        left_extra = vertices[0] + 1.2 * LEFT
        right_extra = vertices[-1] + 1.2 * RIGHT
        all_vertices = [left_extra] + vertices + [right_extra]

        edges = [(i, i + 1) for i in range(len(all_vertices) - 1)]

        graph = Graph(
            vertices=list(range(len(all_vertices))),
            edges=edges,
            layout={i: pos for i, pos in enumerate(all_vertices)},
            vertex_config={"radius": 0.12, "color": COL_LIGHT},
            labels=False
        )
        self.add(graph)
        self.play(FadeOut(question_text), run_time = 0.25)

        
        learn_more_text = (  VGroup(
                    Tex("This is the contact process on $\mathbb{Z}$ with rate $\lambda$").set_color(COL_LIGHT),
                    Tex(r"$\lambda_c := \text{critical value}.$").set_color(COL_LIGHT),
                    ).arrange(DOWN).scale(0.75))
        learn_more_text.to_edge(UP, buff = 2)
        self.play(
            GrowFromCenter(learn_more_text),
            *[m.animate.scale(0) for m in men],
            run_time=1.0
        )
        self.next_slide()  

        learn_more_text = (  VGroup(
                    Tex(r'Below the critical value $\lambda_c$ the infection dies out.', color=COL_LIGHT),
                    Tex(r'Above the critical value $\lambda_c$ the infection has a positive probability of survival.', color=COL_LIGHT),
                    ).arrange(DOWN).scale(0.75))
        learn_more_text.to_edge(DOWN, buff=2)
        self.play(GrowFromCenter(learn_more_text))
        self.next_slide()

        self.wipe(self.mobjects_without_canvas, [])
        self.init_slides("Content")
        self.next_slide()


        flag = ImageMobject(r'C:\Users\caspe\OneDrive\Documents\Universiteit\Scriptie\Python\Visualisations\Eindpresentatie\media\images\Eindpresentatie\flag.png').scale(0.5)
        flag.move_to(ORIGIN + 4 * RIGHT)
        lambda_text = Tex(r'$\lambda_c \geq 0.5$', color=COL_LIGHT).scale(1.25)
        lambda_text.next_to(flag, DOWN, buff=0.3)
        self.play(FadeIn(flag), FadeIn(lambda_text))
        self.next_slide()

        family_tree_text = Text("Family trees", color=COL_LIGHT).scale(0.5)
        positions = { 0: ORIGIN + 4 * LEFT, 1: ORIGIN + 3 * LEFT + DOWN * 1.2, 2: ORIGIN + 5 * LEFT + DOWN * 1.2}
        family_graph = Graph(
            vertices=[0, 1, 2],
            edges=[(0, 1), (0, 2)],
            layout=positions,
            vertex_config={"radius": 0.15, "color": COL_LIGHT},
            labels=False
        )
        names = [
            Text("Father", color=COL_LIGHT).scale(0.4).next_to(positions[0], UP, buff=0.2),
            Text("Casper Algera", color=COL_LIGHT).scale(0.4).next_to(positions[1], DOWN, buff=0.2),
            Text("Son", color=COL_LIGHT).scale(0.4).next_to(positions[2], DOWN, buff=0.2),
        ]
        name_group = VGroup(*names)

        self.play(FadeIn(family_graph), FadeIn(name_group), FadeIn(family_tree_text.move_to(ORIGIN + 4 * LEFT + UP)))
        self.next_slide()

        Connectiontext = Text("Contact process").scale(0.5).move_to(ORIGIN + UP)
        HarrisRepr02 = ImageMobject(r'C:\Users\caspe\OneDrive\Documents\Universiteit\Scriptie\Python\Visualisations\Eindpresentatie\media\images\HarrisRepr_02.png').scale(0.5).next_to(Connectiontext, DOWN*0.8, buff=0.2)
        self.play(FadeIn(Connectiontext), FadeIn(HarrisRepr02))

        self.next_slide()
        arrow1 = Arrow(ORIGIN + 2 * RIGHT + 0.5 * DOWN, ORIGIN + 3 * RIGHT + 0.5 * DOWN, buff=0.1, stroke_width=10)
        arrow2 = Arrow(ORIGIN + 3 * LEFT + 0.5 * DOWN, ORIGIN + 2 * LEFT + 0.5 * DOWN, buff=0.1, stroke_width=10)
        self.play(FadeIn(arrow1), FadeIn(arrow2))
        self.next_slide()

        self.wipe(self.mobjects_without_canvas, [])
        self.init_slides("Family trees")
        family_tree_text = Text("Family trees", color=COL_LIGHT).scale(0.75).move_to(ORIGIN).to_edge(UP, buff=2)
        base_y = 0.5
        y_gap = 0.8
        positions = {
            0: ORIGIN + 2.5 * LEFT + UP * (base_y), 
            1: ORIGIN + 2.5 * LEFT + 2 * LEFT + UP * (base_y - y_gap),  
            2: ORIGIN + 2.5 * LEFT + 2 * RIGHT + UP * (base_y - y_gap), 
            3: ORIGIN + 2.5 * LEFT + 2 * LEFT + UP * (base_y - 2* y_gap),  
            7: ORIGIN + 2.5 * LEFT + 3.5 * RIGHT +UP * (base_y - 2 * y_gap),  
            6: ORIGIN + 2.5 * LEFT + 0.5 * RIGHT +UP * (base_y - 2 * y_gap), 
            4: ORIGIN + 2.5 * LEFT + 2 * RIGHT + UP * (base_y - 2 * y_gap),  
            5: ORIGIN + 2.5 * LEFT + 2 * RIGHT + UP * (base_y - 3 * y_gap),  
        }
        family_graph = Graph(
            vertices=[0, 1, 2, 3, 4, 5, 6, 7],
            edges=[(0, 1), (0, 2), (1, 3), (2, 4),(2, 6),(2, 7), (4, 5)],
            layout=positions,
            vertex_config={"radius": 0.18, "color": COL_LIGHT},
            labels=False
        )
        names = [
            Text("Edward I", color=COL_LIGHT).scale(0.4).next_to(positions[0], DOWN, buff=0.15),
            Text("Edward II", color=COL_LIGHT).scale(0.4).next_to(positions[1], DOWN, buff=0.15),
            Text("Henry I", color=COL_LIGHT).scale(0.4).next_to(positions[2], DOWN, buff=0.15),
            Text("William I", color=COL_LIGHT).scale(0.4).next_to(positions[3], DOWN, buff=0.15),
            Text("Edward III", color=COL_LIGHT).scale(0.4).next_to(positions[4], DOWN, buff=0.15),
            Text("Alfred I", color=COL_LIGHT).scale(0.4).next_to(positions[7], DOWN, buff=0.15),
            Text("Stephen I", color=COL_LIGHT).scale(0.4).next_to(positions[6], DOWN, buff=0.15),
            Text("Edward IV", color=COL_LIGHT).scale(0.4).next_to(positions[5], DOWN, buff=0.15)
        ]
        name_group = VGroup(*names)

        self.play(FadeIn(family_graph), FadeIn(name_group), FadeIn(family_tree_text))
        self.next_slide()

        new_text = Text("Galton-Watson process", color=COL_LIGHT).move_to(ORIGIN).to_edge(UP, buff=2).scale(0.75)
        self.play(FadeOut(family_graph), FadeOut(name_group), FadeIn(new_text), FadeOut(family_tree_text))
        self.next_slide()

        subgraphs = []
        position_keys = list(positions.keys())
        i = 1
        first_point_graph = Graph(
            vertices=[0],
            edges=[],
            layout={0: positions[0]},
            vertex_config={"radius": 0.18, "color": COL_LIGHT},
            labels=False
        )
        subgraphs.append(first_point_graph)
        self.play(FadeIn(VGroup(*names[0])), FadeIn(subgraphs[0]), run_time=0.5)
        self.next_slide()

        gen_text_lines = [
            r"Random variable $X$ determines the children",
            r"i.i.d. for each node."
        ]
        generation_text = VGroup(
            *[Tex(line, color=COL_LIGHT).scale(0.75) for line in gen_text_lines]
        ).arrange(DOWN, aligned_edge=LEFT).next_to(first_point_graph, RIGHT, buff=1.5)
        self.play(FadeIn(generation_text), run_time=0.5)
        self.next_slide()
        while i < len(position_keys):
            if i == 4:
                i+= 2
            sub_vertices = position_keys[0:i+1] 
            sub_edges = [e for e in [(0, 1), (0, 2), (1, 3), (2, 4), (2, 6), (2, 7), (4, 5)] if e[0] in sub_vertices and e[1] in sub_vertices]
            sub_positions = {j: positions[j] for j in sub_vertices}
            subgraph = Graph(
            vertices=sub_vertices,
            edges=sub_edges,
            layout=sub_positions,
            vertex_config={"radius": 0.18, "color": COL_LIGHT},
            labels=False
            )
            subgraphs.append(subgraph)
            i += 1

        i = 1
        while i < len(subgraphs) - 1:
            if i == 1:
                self.play(FadeIn(VGroup(*names[i:i+2])), FadeOut(subgraphs[i]), FadeIn(subgraphs[i+1]), run_time=0.5)
            elif i == 3:
                self.play(FadeIn(VGroup(*names[i+1:i+4])), FadeOut(subgraphs[i]), FadeIn(subgraphs[i+1]), run_time=0.5)
            elif i > 3:
                self.play(FadeIn(VGroup(*names[-1])), FadeOut(subgraphs[i]), FadeIn(subgraphs[i+1]), run_time=0.5)
            elif i != 0:
                self.play(FadeIn(VGroup(*names[i + 1:i+2])), FadeOut(subgraphs[i]), FadeIn(subgraphs[i+1]), run_time=0.5)
            i += 1
            self.next_slide()


        third_gen_indices = [3, 4, 6, 7]
        third_gen_positions = [positions[i] for i in third_gen_indices]
        min_x = min(pos[0] for pos in third_gen_positions)
        max_x = max(pos[0] for pos in third_gen_positions)
        min_y = min(pos[1] for pos in third_gen_positions)
        max_y = max(pos[1] for pos in third_gen_positions)
        pad_x = 0.7
        pad_y = 0.4
        rect = Rectangle(
            width=(max_x - min_x) + 2 * pad_x,
            height=(max_y - min_y) + 2 * pad_y,
            stroke_color=YELLOW,
            stroke_width=4
        ).move_to(((min_x + max_x) / 2, (min_y + max_y-0.1) / 2, 0))
        generation_text = Tex(r"Generation $Z_2$.", color=COL_LIGHT).scale(0.75).next_to(rect, RIGHT, buff=0.5)
        self.play(Create(rect), FadeIn(generation_text))

        self.next_slide()
        self.wipe(self.mobjects_without_canvas, [])
        self.init_slides("Extinction of the tree")

        tex_lines = [
            r"$\cdot$ Let $Z_n$ be the number of individuals in the $n$-th generation.",
            r"$\mathbb{E} \left[ Z_n \right] = \sum_{m \in \mathbb{N}} \mathbb{E} \left[ Z_n \mid Z_{n-1} = m \right] \mathbb{P}\left[Z_{n-1} = m\right]$",
            r"$= \sum_{m \in \mathbb{N}} m \mathbb{E} \left[ X \right] \mathbb{P}\left[Z_{n-1} = m\right]$",
            r"$= \mathbb{E} \left[ X \right] \mathbb{E} \left[ Z_{n-1} \right]$.",
            r"$\cdot$ So that, by induction,",
            r"$\mathbb{E} \left[ Z_n \right] = \mathbb{E} \left[ X \right]^n.$",
        ]
        tex_mobs = []
        for i, line in enumerate(tex_lines):
            mob = Tex(line, tex_template=TexTemplate(preamble=r"\usepackage{amssymb}"), color=COL_LIGHT).scale(0.7).to_edge(UP, buff=2).shift(DOWN * i * 0.7).align_on_border(LEFT, buff=0.5)
            if line.lstrip().startswith('$='):
                mob.shift(RIGHT * 1)
            tex_mobs.append(mob)
            run_time = max(0.2, min(5, len(line) * 0.015))
            self.play(Write(mob, run_time=run_time))
            self.next_slide()
        self.play(*[FadeOut(mob) for mob in tex_mobs[:-1]], run_time=0.5)
        self.play(tex_mobs[-1].animate.to_edge(UP, buff=2), run_time=0.5)
        self.next_slide()
        text_code_2_lines = [

            r"$\cdot$ Now suppose that $\mathbb{E} \left[ X \right] < 1$, then by the Markov inequality,",
            r"$\lim_{n \to \infty}  \mathbb{P}\left[Z_n \geq 1\right] \leq \lim_{n \to \infty} \mathbb{E} \left[ Z_n \right] =  \lim_{n \to \infty} \mathbb{E} \left[ X \right]^n = 0$.",
            r"$\cdot$ Hence, $\lim_{n \to \infty} \mathbb{P}\left[Z_n = 0\right] = 1$."
        ]
        prev_mob = tex_mobs[-1]
        for i, line in enumerate(text_code_2_lines):
            mob = Tex(line, tex_template=TexTemplate(preamble=r"\usepackage{amssymb}"), color=COL_LIGHT).scale(0.7).next_to(prev_mob, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
            run_time = max(0.2, min(5, len(line) * 0.015))
            self.play(Write(mob, run_time=run_time))
            self.next_slide()
            prev_mob = mob

        final_text = Tex(r"If $\mathbb{E} \left[ X \right] < 1$, then extinction occurs with probability 1!", color=YELLOW).scale(1).next_to(prev_mob, DOWN, buff=1).align_on_border(LEFT, buff=0.5).shift(RIGHT*0.8)
        self.play(FadeIn(final_text))
        self.next_slide()


        self.wipe(self.mobjects_without_canvas, [])
        self.init_slides("Memoryless property")
        self.memoryless()
        self.next_slide()


        self.wipe(self.mobjects_without_canvas, [])
        self.init_slides("Contact process")
        Text1 = Tex(r"$\cdot$ We now define the contact process with rate $\lambda$.", color=COL_LIGHT).scale(0.75).to_edge(UP, buff=2.5).align_on_border(LEFT, buff=0.5)
        self.play(Write(Text1), runtime = 0.5)
        self.next_slide()
        Text2 = Tex(r"$\cdot$ The set of infected nodes is $I_t \subset \mathbb{Z}$.", color=COL_LIGHT).scale(0.75).next_to(Text1, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(Write(Text2), runtime = 0.5)
        self.next_slide()
        Text3 = Tex(r"$\cdot$ Infected nodes in $I_t$ heal after time sampled from $\textit{Exp}(1)$.", color=COL_LIGHT).scale(0.75).next_to(Text2, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(Write(Text3), runtime = 0.5)
        self.next_slide()
        Text4 = Tex(r"$\cdot$ While $i$ is infected, its neighbours get infected after time sampled from $\textit{Exp}(\lambda)$.", color=COL_LIGHT).scale(0.75).next_to(Text3, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(Write(Text4), runtime = 0.5)
        self.next_slide()
        Text5 = Tex(r"$\cdot$ We also say that recoveries occur at rate $1$ and infection at rate $\lambda$.", color=COL_LIGHT).scale(0.75).next_to(Text4, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(Write(Text5), runtime = 0.5)
        self.next_slide()
        Text6 = Tex(r"$\cdot$ The memoryless property ensures the Markov property $$\mathbb{P}\left[I_{s+t} = A \mid I_{s'} \text{ for } 0 \leq s' \leq s\right] = \mathbb{P}[I_{s+t} = A | I_s]$$", color=COL_LIGHT).scale(0.75).next_to(Text5, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(Write(Text6), runtime = 0.5)
        self.next_slide()

        HarrisRepr00 = ImageMobject(r'C:\Users\caspe\OneDrive\Documents\Universiteit\Scriptie\Python\Visualisations\Eindpresentatie\media\images\HarrisRepr_00.png').to_edge(UP, buff= 2).align_on_border(LEFT, buff=0.5)
        HarrisRepr01 = ImageMobject(r'C:\Users\caspe\OneDrive\Documents\Universiteit\Scriptie\Python\Visualisations\Eindpresentatie\media\images\HarrisRepr_01.png').to_edge(UP, buff= 2).align_on_border(LEFT, buff=0.5)
        HarrisRepr02 = ImageMobject(r'C:\Users\caspe\OneDrive\Documents\Universiteit\Scriptie\Python\Visualisations\Eindpresentatie\media\images\HarrisRepr_02.png').to_edge(UP, buff= 2).align_on_border(LEFT, buff=0.5)
        HarrisRepr03 = ImageMobject(r'C:\Users\caspe\OneDrive\Documents\Universiteit\Scriptie\Python\Visualisations\Eindpresentatie\media\images\HarrisRepr_03.png').to_edge(UP, buff= 2).align_on_border(LEFT, buff=0.5)

        self.wipe(self.mobjects_without_canvas, [])
        self.play(FadeIn(HarrisRepr00))
        self.next_slide()
        poisson_lines = [
            r"Remember that events with",
            r"exponential waiting times,",
            r"can be modeled using",
            r"a Poisson process."
        ]
        PoissonText = VGroup(
            *[Tex(line, color=COL_LIGHT).scale(0.75) for line in poisson_lines]
        ).arrange(DOWN, aligned_edge=LEFT).next_to(HarrisRepr00, RIGHT, buff=0.5)
        self.play(FadeIn(PoissonText), run_time=0.5)
        self.next_slide()
        self.play(FadeIn(HarrisRepr01), run_time=0.5)
        self.next_slide()
        self.play(FadeIn(HarrisRepr02), run_time=0.5)
        self.next_slide()
        self.play(FadeIn(HarrisRepr03), run_time=0.5)
        self.next_slide()
        self.play(FadeOut(HarrisRepr00), FadeOut(HarrisRepr01), FadeOut(HarrisRepr02), FadeOut(HarrisRepr03), FadeOut(PoissonText), run_time=0.5)


        self.init_slides("The critical value")
        self.next_slide()
        critval = Tex("$\cdot$ Remember the change in behaviour.", color=COL_LIGHT).scale(0.7).align_on_border(LEFT, buff=0.5)
        self.play(Write(critval), runtime=0.5)
        self.next_slide()
        critval2 = Tex(r"$\cdot$ The critical value $\lambda_c = \inf \left\{\lambda \mid \lim_{t \to \infty} \mathbb{P}\left[I_t \neq \varnothing \right] > 0 \right\}$.", color=COL_LIGHT).scale(0.7).next_to(critval, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(Write(critval2), runtime=0.5)
        self.next_slide()
        critval3 = Tex(r"$\cdot$ We will show that the contact process surely dies out if $\lambda < \tfrac{1}{2}$.", color=COL_LIGHT).scale(0.7).next_to(critval2, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(Write(critval3), runtime=0.5)
        self.next_slide()



        self.wipe(self.mobjects_without_canvas, [])
        self.init_slides("Completing the proof")

        harris_images = []
        for i in range(11):
            img_path = rf'C:\Users\caspe\OneDrive\Documents\Universiteit\Scriptie\Python\Visualisations\Eindpresentatie\media\images\HarrisRepr_coupling_{i:02d}.png'
            img = ImageMobject(img_path).to_edge(UP, buff=2).align_on_border(LEFT, buff=0.5)
            harris_images.append(img)

        gw_images = []
        for i in range(10):
            img_path = rf'C:\Users\caspe\OneDrive\Documents\Universiteit\Scriptie\Python\Visualisations\Eindpresentatie\media\images\GWtreepres_{i:02d}.png'
            img = ImageMobject(img_path).to_edge(UP, buff=1.2).align_on_border(RIGHT, buff=0.5).scale(0.75)
            gw_images.append(img)

        self.play(FadeIn(harris_images[0]))
        self.next_slide()
        poisson_lines = [
            r"Let X be the number",
            r"of infected sites after",
            r"one infection or recovery."
        ]
        PoissonText = VGroup(
            *[Tex(line, color=COL_LIGHT).scale(0.75) for line in poisson_lines]
        ).arrange(DOWN, aligned_edge=LEFT).next_to(harris_images[0], RIGHT, buff=0.5).shift(UP * 1.8)

        self.play(FadeIn(PoissonText), run_time=0.5)
        self.next_slide()

        cover_rects = [
            Rectangle(
            width=img.width,
            height=img.height,
            fill_color=COL_DARK,
            fill_opacity=1,
            stroke_width=0
            ).move_to(img.get_center())
            for img in harris_images
        ]

        cover_rects2 = [
            Rectangle(
            width=img.width,
            height=img.height * 0.66,
            fill_color=COL_DARK,
            fill_opacity=1,
            stroke_width=0
            ).move_to(img.get_center()).shift(DOWN)
            for img in gw_images
        ]

        for i in range(1, len(harris_images)):
            if i < 4:
                self.play(FadeIn(cover_rects[i]), FadeIn(harris_images[i]), FadeIn(cover_rects2[i]), FadeIn(gw_images[i]), run_time=0.5)
            if i == 4:
                self.play(FadeIn(cover_rects[i]), FadeIn(harris_images[i]), run_time=0.5)
            if i > 4:
                self.play(FadeIn(cover_rects[i]), FadeIn(harris_images[i]), FadeIn(cover_rects2[i - 1]), FadeIn(gw_images[i - 1]), run_time=0.5)
            self.next_slide()
        self.play(FadeOut(harris_images[-1]), FadeOut(gw_images[-1]), FadeOut(PoissonText), run_time=0.5)


        self.wipe(self.mobjects_without_canvas, [])

        tex_lines = [
            r"$\cdot$ We have shown that the Galton-Watson tree dies out if $\mathbb{E}[X] < 1$.",
            r"$\mathbb{E} \left[ X \right] = 2\mathbb{P}[\textit{infection before recovery}]$",
            r"$\cdot$ The waiting time of an infection any neighbour is given by $Y \sim \textit{Exp}(2\lambda)$",
            r"$\cdot$ The waiting time of recovery is given by $Z \sim \textit{Exp}(1)$.",
            r"$\mathbb{P}[\textit{infection before recovery}] = \mathbb{P}[Y < Z] = \frac{2\lambda}{2\lambda + 1}.$",
            r"$\cdot$ This gives $\mathbb{E}[X] = \frac{4\lambda}{2\lambda + 1}.$",
            r"$\cdot$ Finally, $\mathbb{E}[X] < 1 \Rightarrow \frac{4\lambda}{2\lambda + 1} < 1 \Rightarrow \lambda < \frac{1}{2}.$",
            r"$\cdot$ Thus, the contact process dies out if $\lambda < \frac{1}{2}$."
        ]
        tex_mobs = []
        for i, line in enumerate(tex_lines):
            mob = Tex(line, tex_template=TexTemplate(preamble=r"\usepackage{amssymb}"), color=COL_LIGHT).scale(0.7).to_edge(UP, buff=2).shift(DOWN * i * 0.5).align_on_border(LEFT, buff=0.5)
            if line.lstrip().startswith('$='):
                mob.shift(RIGHT * 1)
            tex_mobs.append(mob)
            run_time = max(0.2, min(5, len(line) * 0.015))
            self.play(Write(mob, run_time=run_time))
            self.next_slide()
        self.play(*[FadeOut(mob) for mob in tex_mobs[:-1]], run_time=0.5)
        self.play(tex_mobs[-1].animate.to_edge(UP, buff=2), run_time=0.5)
        self.init_slides("Finishing up")

        self.next_slide()
        final_line = Tex(r"$\cdot$ This shows $\lambda_c \geq \tfrac{1}{2}$, completing the proof.", color=COL_LIGHT).scale(0.7).next_to(tex_mobs[-1], DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(FadeIn(final_line))
        self.next_slide()
        final_line_2 = Tex(r"$\cdot$ This illustrates a powerful technique called coupling.", color=COL_LIGHT).scale(0.7).next_to(final_line, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(FadeIn(final_line_2))
        self.next_slide()
        final_line_3 = Tex(r"$\cdot$ In my thesis, we use this coupling to show better lower bounds.", color=COL_LIGHT).scale(0.7).next_to(final_line_2, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(FadeIn(final_line_3))
        self.next_slide()
        final_line_4 = Tex(r"$\cdot$ Acknowledgements.", color=COL_LIGHT).scale(0.7).next_to(final_line_3, DOWN, buff=0.2).align_on_border(LEFT, buff=0.5)
        self.play(FadeIn(final_line_4))
        self.next_slide()
        
        self.wipe(self.mobjects, [])
        learn_more_text = Tex("Thank you for your attention!", color=COL_LIGHT).scale(1.5).to_edge(UP, buff=2)
        self.play(GrowFromCenter(learn_more_text))
