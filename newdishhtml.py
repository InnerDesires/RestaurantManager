# encoding: utf-8

from newhtml import HtmlCreator
import os

img_path = os.getcwd() + '\\images\\logo_2.jpg'
css_path = os.getcwd() + '\\files\\style.css'


class DishesHTMLReport(HtmlCreator):

    def design_header(self):
        """Design a header for restaurant manager report."""
        # First, get a css content.
        with open(css_path, 'r') as f:
            css_raw_content = f.read()
        with self.tag('head'):
            self.doc.asis('<meta charset="UTF-8">')
            self.doc.asis('<style>%s</style>' % css_raw_content)
            with self.tag('title'):
                self.text('Restaurant manager report')

    def design_body(self):
        """Design a body of restaurant manager report."""
        tag, text = self.tag, self.text
        data = self.data

        with tag('body', style="padding: 30px;"):
            with tag('table', style='width:100%'):
                with tag('tr'):
                    with tag('td', klass='about'):
                        text('Замовник:', data['about']['client'])
                    with tag('td', klass="logo", rowspan="7", colspan="5"):
                        self.doc.stag('img', src=img_path, alt="Vine e Cucina restaurant")
                with tag('tr'):
                    with tag('td', klass='about'):
                        text('Менеджер: ', data['about']['manager'])
                with tag('tr'):
                    with tag('td', klass='about'):
                        text('Місце проведення: ', data['about']['location'])
                with tag('tr'):
                    with tag('td', klass='about'):
                        text('Дата: ', data['about']['date'])
                with tag('tr'):
                    with tag('td', klass='about'):
                        text('Вид заходу: ', data['about']['type'])
                with tag('tr'):
                    with tag('td', klass='about'):
                        text('Час: ', data['about']['time'])
                with tag('tr'):
                    with tag('td', klass='about'):
                        text('Кількість персон: ', data['about']['persons'])
                with tag('tr'):
                    with tag('td', klass='top-header', colspan='6'):
                        text('Ми щиро вдячні Вам, що обрали саме нас!')
                with tag('tr'):
                    with tag('td', klass='top-header', colspan='6', height='50px'):
                        text('Керуючись Вашими пріорітетами та вподобаннями, ми підготували данну пропозицію.')
                with tag('tr', klass='header'):
                    with tag('th', width='40%'):
                        text('Назва')
                    with tag('th', width='5%'):
                        text('Вихід')
                    with tag('th', width='5%'):
                        text('Кількість')
                    with tag('th', width='20%'):
                        text('Коментар')
                    with tag('th', width='15%'):
                        text('Ціна, грн')
                    with tag('th', width='15%'):
                        text('Сума, грн')

                types = {}
                for dish in data['dishes']:
                    specific_type = data['dishes'][dish]['type']
                    types[specific_type] = {}
                for dish in data['dishes']:
                    specific_type = data['dishes'][dish]['type']
                    specific_dish = {dish: data['dishes'][dish]}
                    types[specific_type].update(specific_dish)

                first_page_max_amount = 26
                is_first_page = True
                next_pages_max_amount = 64
                tmp = 0
                for type in types:
                    with tag("tr", klass='header_line'):
                        if tmp % next_pages_max_amount == 0 and not is_first_page:
                            with tag('tr', height='60px'):
                                for i in range(6):
                                    with tag('td', klass="full_empty"):
                                        text('')
                        if tmp == first_page_max_amount and is_first_page:
                            is_first_page = False
                            with tag('tr', height='60px'):
                                for i in range(6):
                                    with tag('td', klass="full_empty"):
                                        text('')
                        with tag('th'):
                            text(type)
                        for i in range(5):
                            with tag('th'):
                                text("")
                    for dish in types[type]:
                        if tmp % next_pages_max_amount == 0 and not is_first_page:
                            with tag('tr', height='60px'):
                                for i in range(6):
                                    with tag('td', klass="full_empty"):
                                        text('')
                        if tmp == first_page_max_amount and is_first_page:
                            is_first_page = False
                            with tag('tr', height='60px'):
                                for i in range(6):
                                    with tag('td', klass="full_empty"):
                                        text('')
                        with tag('tr', klass='order_line'):
                            tmp += 1
                            with tag('td', klass='name'):
                                text(dish)
                            with tag('td'):
                                text(types[type][dish]['weight'])
                            with tag('td'):
                                text(types[type][dish]['amount'])
                            with tag('td'):
                                text(types[type][dish]['comment'])
                            with tag('td'):
                                text(types[type][dish]['price'])
                            with tag('td'):
                                text(types[type][dish]['total'])

                total_cost = float(data['global']['totalsum'])
                with tag("tr"):
                    with tag('td', klass="total"):
                        text('Загальна сума без обслуговування:')
                    for i in range(4):
                        with tag('td', klass="total"):
                            text("")
                    with tag('td', klass="total"):
                        text('%.2f' % total_cost)
                with tag("tr"):
                    with tag('td', klass="total"):
                        text('Обслуговування 10%:')
                    for i in range(4):
                        with tag('td', klass="total"):
                            text("")
                    with tag('td', klass="total"):
                        tips = 0.1 * total_cost
                        text('%.2f' % tips)
                with tag("tr"):
                    with tag('td', klass="total"):
                        text('Загальна сума:')
                    for i in range(4):
                        with tag('td', klass="total"):
                            text("")
                    with tag('td', klass="total"):
                        text('%.2f' % ((0.1 * total_cost) + total_cost))
                # Add CUSTOM entries here.
                for entry in data['global']['centries']:
                    with tag('tr'):
                        for entry_field in entry:
                            with tag('td', klass='total'):
                                text(entry_field)
                # Add WEIGHT_PER_PERSON entry here.
                # If weight_tracked flag is on, count average weight per person.
                if data['global']['trackw']:
                    # First, count total weight.
                    # TODO: add more dishes to the restricted list.
                    restricted_dishes = ['Ранкова домашня випічка']
                    total_weight = 0
                    for dish in data['dishes']:
                        if data['dishes'][dish]['type'] in restricted_dishes:
                            continue
                        weight_str = str(data['dishes'][dish]['weight'])
                        weight_str_splitted = weight_str.split('/')
                        for value in weight_str_splitted:
                            if value.isdigit():
                                specific_dish_amount = data['dishes'][dish]['amount']
                                total_weight += int(value) * int(specific_dish_amount)
                    # Pass data to the new entry in the table.
                    with tag('tr'):
                        with tag('td', klass="total"):
                            text('Середня вага на особу')
                        for i in range(4):
                            with tag('td', klass="total"):
                                text('')
                        with tag('td', klass="total"):
                            if self.data['about']['persons']:
                                weight_per_person = total_weight / float(self.data['about']['persons'])
                                text('%.2f г' % weight_per_person)
                            else:
                                text('0')

                with tag("tr"):
                    with tag('td', klass="total_per_person_text"):
                        text('Середній рахунок на одну особу')
                    for i in range(4):
                        with tag('td', klass="total_empty"):
                            text("")
                    with tag('td', klass="total_per_person_number"):
                        total_and_tips = tips + total_cost
                        if self.data['about']['persons']:
                            mid_per_person = total_and_tips / float(self.data['about']['persons'])
                            text('%.2f' % mid_per_person)
                        else:
                            text('0')
