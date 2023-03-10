##############################################################################
#
# A Django view class to write an Excel file using the XlsxWriter
# module.
#
# Copyright 2013-2020, John McNamara, jmcnamara@cpan.org
#
import io
from django.http import HttpResponse
import xlsxwriter
import xlwt

from datetime import datetime
from django.db.models import Q, F, Max, Sum, When, Case
from django.views.generic import View

from company.models import Company
from project.models import (Project, ProjectIncBudget, Site, SiteOwner, SiteContract,
                            UnitType, KeyUnit, BuildingUnit, HouseUnit, ProjectOutBudget)
from contract.models import Contract, Contractor, ContractorRelease
from cash.models import CashBook, ProjectCashBook

TODAY = datetime.today().strftime('%Y-%m-%d')


class ExportContracts(View):
    """계약자 리스트"""

    def get(self, request):

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('계약목록_정보')

        worksheet.set_default_row(20)

        project = Project.objects.get(pk=request.GET.get('project'))
        cols = sorted(list(map(int, request.GET.get('col').split('-'))))

        # 1. Title
        row_num = 0
        title_format = workbook.add_format()
        worksheet.set_row(row_num, 50)
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        title_format.set_bold()
        worksheet.merge_range(row_num, 0, row_num, len(cols), str(project) + ' 계약자 리스트', title_format)

        # 2. Header
        row_num = 1
        worksheet.set_row(row_num, 18)
        worksheet.write(row_num, len(cols), TODAY + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header
        row_num = 2
        worksheet.set_row(row_num, 25, workbook.add_format({'bold': True}))

        # title_list
        data_source = [[],
                       ['일련번호', 'serial_number', 10],
                       ['인가여부', 'contractor__is_registed', 8],
                       ['차수', 'order_group__order_group_name', 10],
                       ['타입', 'keyunit__unit_type__name', 7],
                       ['동', 'keyunit__houseunit__building_unit__name', 7],
                       ['호수', 'keyunit__houseunit__name', 7],
                       ['계약자', 'contractor__name', 10],
                       ['생년월일', 'contractor__birth_date', 12],
                       ['계약일자', 'contractor__contract_date', 12],
                       ['연락처[1]', 'contractor__contractorcontact__cell_phone', 14],
                       ['연락처[2]', 'contractor__contractorcontact__home_phone', 14],
                       ['연락처[3]', 'contractor__contractorcontact__other_phone', 14],
                       ['이메일', 'contractor__contractorcontact__email', 15],
                       ['주소[등본]', 'contractor__contractoraddress__id_zipcode', 7],
                       ['', 'contractor__contractoraddress__id_address1', 35],
                       ['', 'contractor__contractoraddress__id_address2', 20],
                       ['', 'contractor__contractoraddress__id_address3', 40],
                       ['주소[우편]', 'contractor__contractoraddress__dm_zipcode', 7],
                       ['', 'contractor__contractoraddress__dm_address1', 35],
                       ['', 'contractor__contractoraddress__dm_address2', 20],
                       ['', 'contractor__contractoraddress__dm_address3', 40],
                       ['비고', 'contractor__note', 45]]

        titles = ['No']
        params = []
        widths = [7]

        for i in cols:  # 요청된 컬럼 개수 만큼 반복 (1-2-3... -> i)
            titles.append(data_source[i][0])  # 일련번호
            params.append(data_source[i][1])  # serial_number
            widths.append(data_source[i][2])  # 10

        h_format = workbook.add_format()
        h_format.set_bold()
        h_format.set_border()
        h_format.set_align('center')
        h_format.set_align('vcenter')
        h_format.set_bg_color('#eeeeee')

        # Adjust the column width.
        for i, cw in enumerate(widths):  # 각 컬럼 넙이 세팅
            worksheet.set_column(i, i, cw)

        # Write header
        for col_num, col in enumerate(titles):  # 헤더 줄 제목 세팅
            if '주소' in col:
                worksheet.merge_range(row_num, col_num, row_num, col_num + 3, titles[col_num], h_format)
            else:
                worksheet.write(row_num, col_num, titles[col_num], h_format)

        # 4. Body
        # Get some data to write to the spreadsheet.
        data = Contract.objects.filter(project=project,
                                       keyunit__contract__isnull=False,
                                       contractor__status='2').order_by('contractor__contract_date')
        if request.GET.get('group'):
            data = data.filter(order_group=request.GET.get('group'))
        if request.GET.get('type'):
            data = data.filter(keyunit__unit_type=request.GET.get('type'))
        if self.request.GET.get('dong'):
            data = data.filter(keyunit__houseunit__building_unit=self.request.GET.get('dong'))
        if request.GET.get('status'):
            data = data.filter(contractor__status=request.GET.get('status'))
        if request.GET.get('null'):
            is_null = True if request.GET.get('null') == '1' else False
            data = data.filter(keyunit__houseunit__isnull=is_null)
        if request.GET.get('reg'):
            result = True if request.GET.get('reg') == '1' else False
            data = data.filter(contractor__is_registed=result)
        order_list = ['-created_at', 'created_at', '-contractor__contract_date',
                      'contractor__contract_date', '-serial_number',
                      'serial_number', '-contractor__name', 'contractor__name']
        if self.request.GET.get('order'):
            data = data.order_by(order_list[int(self.request.GET.get('order'))])
        if request.GET.get('sdate'):
            data = data.filter(contractor__contract_date__gte=request.GET.get('sdate'))
        if request.GET.get('edate'):
            data = data.filter(contractor__contract_date__lte=request.GET.get('edate'))
        if request.GET.get('q'):
            data = data.filter(
                Q(serial_number__icontains=request.GET.get('q')) |
                Q(contractor__name__icontains=request.GET.get('q')) |
                Q(contractor__note__icontains=request.GET.get('q')))

        data = data.values_list(*params)

        b_format = workbook.add_format()
        b_format.set_align('vcenter')
        b_format.set_border()
        b_format.set_num_format('yyyy-mm-dd')
        b_format.set_align('center')

        body_format = {
            'border': True,
            'valign': 'vcenter',
            'num_format': 'yyyy-mm-dd',
            'align': 'center',
        }

        is_reg = []  # ('인가여부',)
        is_date = []  # ('생년월일', '계약일자')
        reg_data = ('미인가', '인가')
        is_left = []

        # Write body
        for col_num, col in enumerate(titles):
            if col == '인가여부':
                is_reg.append(col_num)
            if col in ('생년월일', '계약일자'):
                is_date.append(col_num)
            if col in ('', '비고'):
                is_left.append(col_num)

        for i, row in enumerate(data):
            row = list(row)
            row_num += 1
            row.insert(0, i + 1)
            for col_num, cell_data in enumerate(row):
                if col_num == 0:
                    body_format['num_format'] = '#,##0'
                else:
                    body_format['num_format'] = 'yyyy-mm-dd'
                if col_num in is_reg:  # 인가 여부 데이터 치환
                    cell_data = reg_data[int(cell_data)]
                if col_num in is_left:
                    if 'align' in body_format:
                        del body_format['align']
                else:
                    if 'align' not in body_format:
                        body_format['align'] = 'center'
                bf = workbook.add_format(body_format)
                worksheet.write(row_num, col_num, cell_data, bf)

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = '{date}-contracts.xlsx'.format(date=datetime.now().strftime('%Y-%m-%d'))
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


class ExportApplicants(View):
    """청약자 리스트"""

    def get(self, request):

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('청약목록_정보')

        worksheet.set_default_row(20)

        project = Project.objects.get(pk=request.GET.get('project'))

        # title_list
        data_source = [[],
                       ['일련번호', 'serial_number', 10],
                       ['차수', 'order_group__order_group_name', 10],
                       ['타입', 'keyunit__unit_type__name', 7],
                       ['청약자', 'contractor__name', 10],
                       ['청약일자', 'contractor__reservation_date', 12],
                       ['연락처[1]', 'contractor__contractorcontact__cell_phone', 14],
                       ['연락처[2]', 'contractor__contractorcontact__home_phone', 14],
                       ['연락처[3]', 'contractor__contractorcontact__other_phone', 14],
                       ['이메일', 'contractor__contractorcontact__email', 15],
                       ['비고', 'contractor__note', 45]]

        if project.is_unit_set:
            data_source.append(
                ['동', 'keyunit__houseunit__building_unit', 7],
                ['호수', 'keyunit__houseunit__name', 7]
            )

        # 1. Title
        row_num = 0
        worksheet.set_row(row_num, 50)
        title_format = workbook.add_format()
        title_format.set_bold()
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        worksheet.merge_range(row_num, 0, row_num, len(data_source) - 1, str(project) + ' 청약자 리스트', title_format)

        # 2. Pre Header - Date
        row_num = 1
        worksheet.set_row(row_num, 18)
        worksheet.write(row_num, len(data_source) - 1, TODAY + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header
        row_num = 2
        worksheet.set_row(row_num, 25, workbook.add_format({'bold': True}))

        titles = ['No']  # header titles
        params = []  # ORM 추출 field
        widths = [7]  # No. 컬럼 넓이

        for ds in data_source:
            if ds:
                titles.append(ds[0])
                params.append(ds[1])
                widths.append(ds[2])

        h_format = workbook.add_format()
        h_format.set_bold()
        h_format.set_border()
        h_format.set_align('center')
        h_format.set_align('vcenter')
        h_format.set_bg_color('#eeeeee')

        # Adjust the column width.
        for i, col_width in enumerate(widths):
            worksheet.set_column(i, i, col_width)

        # Write header
        for col_num, col in enumerate(titles):
            worksheet.write(row_num, col_num, titles[col_num], h_format)

        # 4. Body
        # Get some data to write to the spreadsheet.
        data = Contract.objects.filter(project=project,
                                       keyunit__contract__isnull=False,
                                       contractor__status='1')

        data = data.values_list(*params)

        b_format = workbook.add_format()
        b_format.set_border()
        b_format.set_align('center')
        b_format.set_align('vcenter')
        b_format.set_num_format('yyyy-mm-dd')

        body_format = {
            'border': True,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': 'yyyy-mm-dd'
        }

        is_left = []
        # Write header
        for col_num, col in enumerate(titles):
            if col in ('비고'):
                is_left.append(col_num)

        # Write header
        for i, row in enumerate(data):
            row = list(row)
            row_num += 1
            row.insert(0, i + 1)
            for col_num, cell_data in enumerate(row):
                if col_num == 0:
                    body_format['num_format'] = '#,##0'
                else:
                    body_format['num_format'] = 'yyyy-mm-dd'
                if col_num in is_left:
                    if 'align' in body_format:
                        del body_format['align']
                else:
                    if 'align' not in body_format:
                        body_format['align'] = 'center'
                bformat = workbook.add_format(body_format)
                worksheet.write(row_num, col_num, cell_data, bformat)

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = '{date}-applicants.xlsx'.format(date=datetime.now().strftime('%Y-%m-%d'))
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


class ExportReleases(View):
    """해지자 리스트"""

    def get(self, request):

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('해지자목록_정보')

        worksheet.set_default_row(20)

        project = Project.objects.get(pk=request.GET.get('project'))

        # title_list
        data_source = [[],
                       ['해지자', 'contractor__name', 10],
                       ['해지일련번호', 'contractor__contract__serial_number', 30],
                       ['현재상태', 'status', 12],
                       ['환불(예정)금액', 'refund_amount', 15],
                       ['은행', 'refund_account_bank', 15],
                       ['계좌번호', 'refund_account_number', 18],
                       ['예금주', 'refund_account_depositor', 12],
                       ['해지신청일', 'request_date', 14],
                       ['환불처리일', 'completion_date', 14],
                       ['비고', 'note', 45]]

        # 1. Title
        row_num = 0
        worksheet.set_row(row_num, 50)
        title_format = workbook.add_format()
        title_format.set_bold()
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        worksheet.merge_range(row_num, 0, row_num, len(data_source) - 1, str(project) + ' 해지자 리스트', title_format)

        # 2. Pre Header - Date
        row_num = 1
        worksheet.set_row(row_num, 18)
        worksheet.write(row_num, len(data_source) - 1, TODAY + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header - 1
        row_num = 2
        worksheet.set_row(row_num, 20, workbook.add_format({'bold': True}))

        titles = ['No']  # header titles
        params = []  # ORM 추출 field
        widths = [7]  # No. 컬럼 넓이

        for ds in data_source:
            if ds:
                titles.append(ds[0])
                params.append(ds[1])
                widths.append(ds[2])

        h_format = workbook.add_format()
        h_format.set_bold()
        h_format.set_border()
        h_format.set_align('center')
        h_format.set_align('vcenter')
        h_format.set_bg_color('#eeeeee')

        # Adjust the column width.
        for i, col_width in enumerate(widths):
            worksheet.set_column(i, i, col_width)

        # Write header - 1
        for col_num, title in enumerate(titles):
            if col_num == 5:
                worksheet.merge_range(row_num, col_num, row_num, col_num + 2, '환불 계좌', h_format)
            elif col_num in [6, 7]:
                pass
            else:
                worksheet.write(row_num, col_num, title, h_format)

        # Write Header - 2
        row_num = 3
        for col_num, title in enumerate(titles):
            if col_num in [5, 6, 7]:
                worksheet.write(row_num, col_num, title, h_format)
            else:
                worksheet.merge_range(row_num - 1, col_num, row_num, col_num, title, h_format)

        # 4. Body
        # Get some data to write to the spreadsheet.
        data = ContractorRelease.objects.filter(project=project, status__gte='3')

        data = data.values_list(*params)

        b_format = workbook.add_format()
        b_format.set_border()
        b_format.set_align('center')
        b_format.set_align('vcenter')
        b_format.set_num_format('yyyy-mm-dd')

        body_format = {
            'border': True,
            'valign': 'vcenter',
            'num_format': 'yyyy-mm-dd'
        }

        # Write header
        choice = dict(ContractorRelease.STATUS_CHOICES)
        for i, row in enumerate(data):
            row = list(row)
            row_num += 1
            row.insert(0, i + 1)
            for col_num, cell_data in enumerate(row):
                if col_num in [0, 4]:
                    body_format['num_format'] = '#,##0'
                else:
                    body_format['num_format'] = 'yyyy-mm-dd'
                if col_num == 4:
                    body_format['align'] = 'right'
                elif col_num == 10:
                    body_format['align'] = 'left'
                else:
                    body_format['align'] = 'center'
                if col_num == 3:
                    cell_data = choice[cell_data]
                bformat = workbook.add_format(body_format)
                worksheet.write(row_num, col_num, cell_data, bformat)

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = '{date}-releases.xlsx'.format(date=datetime.now().strftime('%Y-%m-%d'))
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


class ExportUnitStatus(View):
    """동호수 현황표"""

    def get(self, request):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('동호수현황표')

        worksheet.set_default_row(15)

        ### data start --------------------------------------------- #
        project = Project.objects.get(pk=request.GET.get('project'))
        max_floor = HouseUnit.objects.aggregate(Max('floor_no'))
        floor_no__max = max_floor['floor_no__max'] if max_floor['floor_no__max'] else 1
        max_floor_range = range(0, floor_no__max)
        unit_numbers = HouseUnit.objects.filter(project=project)
        dong_obj = BuildingUnit.objects.filter(project=project).values('name')

        # 1. Title
        row_num = 0
        title_format = workbook.add_format()
        worksheet.set_row(row_num, 50)
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        title_format.set_bold()

        worksheet.write(row_num, 0, str(project) + ' 동호수 현황표', title_format)

        # 2. Sub Description
        max_col = 0
        row_num = 1

        for dong in dong_obj:
            lines = unit_numbers.order_by('bldg_line').values('bldg_line').filter(
                building_unit__name__contains=dong['name']).distinct()
            for line in lines:
                max_col += 1
            max_col += 1

        worksheet.write(row_num, max_col, TODAY + ' 현재', workbook.add_format({'align': 'right', 'font_size': '9'}))

        # 3. Unit status board
        row_num = 3
        worksheet.set_column(0, max_col, 5.5)
        unit_format = {
            'border': True,
            'font_size': 8,
            'align': 'center',
            'valign': 'vcenter'
        }
        status_format = {
            'border': True,
            'font_size': 8,
            'align': 'center',
            'valign': 'vcenter'
        }
        # 최고층수 만큼 반복
        for mf in max_floor_range:
            row_num += 2
            floor_no = floor_no__max - mf  # 현재 층수
            col_num = 1
            # 동 수 만큼 반복
            for dong in dong_obj:  # 동호수 표시 라인
                units = unit_numbers.filter(building_unit__name=dong['name'])
                lines = unit_numbers.order_by('bldg_line').values('bldg_line').filter(
                    building_unit__name__contains=dong['name']).distinct()
                for line in lines:
                    try:
                        unit = units.get(floor_no=floor_no, bldg_line=line['bldg_line'])
                    except:
                        unit = None
                    if unit or floor_no <= 2:
                        unit_format['bg_color'] = unit.unit_type.color if unit else '#dddddd'
                        unit_formats = workbook.add_format(unit_format)
                        if not unit:
                            worksheet.merge_range(row_num, col_num, row_num + 1, col_num, '', unit_formats)
                        else:
                            worksheet.write(row_num, col_num, int(unit.name), unit_formats)
                            if unit.key_unit:
                                if int(unit.key_unit.contract.contractor.status) % 2 == 0:
                                    status_format['bg_color'] = '#85929E'
                                    status_format['font_color'] = 'white'
                                else:
                                    status_format['bg_color'] = '#DAF7A6'
                                    status_format['font_color'] = 'black'
                            else:
                                status_format['bg_color'] = 'white'
                            cont = unit.key_unit.contract.contractor.name if unit.key_unit else ''
                            status_formats = workbook.add_format(status_format)
                            worksheet.write(row_num + 1, col_num, cont, status_formats)
                    col_num += 1
                col_num += 1

        row_num += 2
        col_num = 1

        dong_title_format = workbook.add_format()
        dong_title_format.set_bold()
        dong_title_format.set_border()
        dong_title_format.set_font_size(11)
        dong_title_format.set_align('center')
        dong_title_format.set_align('vcenter')
        dong_title_format.set_bg_color('#bbbbbb')

        # 동 수 만큼 반복
        for dong in dong_obj:  # 호수 상태 표시 라인
            lines = unit_numbers.order_by('-bldg_line').values('bldg_line').filter(
                building_unit__name__contains=dong['name']).distinct()
            worksheet.merge_range(row_num, col_num, row_num + 1, col_num + lines.count() - 1,
                                  dong['name'] + '동',
                                  dong_title_format)

            col_num = col_num + lines.count() + 1

        ### data end ----------------------------------------------- #

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = '{date}-unit-status-board.xlsx'.format(date=datetime.now().strftime('%Y-%m-%d'))
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


def export_payments_xls(request):
    """분양대금 수납 내역"""
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename={date}-payments.xls'.format(
        date=datetime.now().strftime('%Y-%m-%d'))

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('분양대금납부_내역')  # 시트 이름

    # get_data: ?project=1&sd=2020-12-01&ed=2020-12-02&ipo=4&ba=5&up=on&q=#
    project = Project.objects.get(pk=request.GET.get('project'))
    sd = request.GET.get('sd')
    ed = request.GET.get('ed')
    og = request.GET.get('og')
    ut = request.GET.get('ut')
    ipo = request.GET.get('ipo')
    ba = request.GET.get('ba')
    up = request.GET.get('up')
    q = request.GET.get('q')

    today = TODAY
    sd = sd if sd else '1900-01-01'
    ed = ed if ed else today
    obj_list = ProjectCashBook.objects.filter(project=project, project_account_d2__in=(1, 2),
                                              deal_date__range=(sd, ed)).order_by('-deal_date', '-created_at')

    if og:
        obj_list = obj_list.filter(contract__order_group=og)

    if ut:
        obj_list = obj_list.filter(contract__unit_type=ut)

    if ipo:
        obj_list = obj_list.filter(installment_order_id=ipo)

    if ba:
        obj_list = obj_list.filter(bank_account__id=ba)

    if up:
        obj_list = obj_list.filter(
            (Q(is_contract_payment=False) | Q(contract__isnull=True)) &
            (Q(project_account_d1_id__in=(1, 2)) | Q(project_account_d2_id__in=(1, 2)))
        )

    if q:
        obj_list = obj_list.filter(
            Q(contract__contractor__name__icontains=q) |
            Q(trader__icontains=q) |
            Q(content__icontains=q) |
            Q(note__icontains=q))

    # Sheet Title, first row
    row_num = 0

    style = xlwt.XFStyle()
    style.font.bold = True
    style.font.height = 300
    style.alignment.vert = style.alignment.VERT_CENTER  # 수직정렬

    ws.write(row_num, 0, str(project) + ' 계약자 대금 납부내역', style)
    ws.row(0).height_mismatch = True
    ws.row(0).height = 38 * 20

    # title_list

    resources = [
        ['거래일자', 'deal_date'],
        ['차수', 'contract__order_group__order_group_name'],
        ['타입', 'contract__keyunit__unit_type__name'],
        ['일련번호', 'contract__serial_number'],
        ['계약자', 'contract__contractor__name'],
        ['입금 금액', 'income'],
        ['납입회차', 'installment_order__pay_name'],
        ['수납계좌', 'bank_account__alias_name'],
        ['입금자', 'trader']
    ]

    columns = []
    params = []

    for rsc in resources:
        columns.append(rsc[0])
        params.append(rsc[1])

    rows = obj_list.values_list(*params)

    # Sheet header, second row
    row_num = 1

    style = xlwt.XFStyle()
    style.font.bold = True

    # 테두리 설정
    # 가는 실선 : 1, 작은 굵은 실선 : 2,가는 파선 : 3, 중간가는 파선 : 4, 큰 굵은 실선 : 5, 이중선 : 6,가는 점선 : 7
    # 큰 굵은 점선 : 8,가는 점선 : 9, 굵은 점선 : 10,가는 이중 점선 : 11, 굵은 이중 점선 : 12, 사선 점선 : 13
    style.borders.left = 1
    style.borders.right = 1
    style.borders.top = 1
    style.borders.bottom = 1

    style.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    style.pattern.pattern_fore_colour = xlwt.Style.colour_map['silver_ega']

    style.alignment.vert = style.alignment.VERT_CENTER  # 수직정렬
    style.alignment.horz = style.alignment.HORZ_CENTER  # 수평정렬

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style)

    # Sheet body, remaining rows
    style = xlwt.XFStyle()
    # 테두리 설정
    style.borders.left = 1
    style.borders.right = 1
    style.borders.top = 1
    style.borders.bottom = 1

    style.alignment.vert = style.alignment.VERT_CENTER  # 수직정렬
    # style.alignment.horz = style.alignment.HORZ_CENTER  # 수평정렬

    for row in rows:
        row_num += 1
        for col_num, col in enumerate((columns)):
            row = list(row)

            if col_num == 0:
                style.num_format_str = 'yyyy-mm-dd'
                ws.col(col_num).width = 110 * 30

            if '금액' in col:
                style.num_format_str = '#,##'
                ws.col(col_num).width = 110 * 30

            if col == '차수' or col == '납입회차' or col == '일련번호':
                ws.col(col_num).width = 110 * 30

            if col == '수납계좌':
                ws.col(col_num).width = 170 * 30

            if col == '입금자' or col == '계약자':
                ws.col(col_num).width = 110 * 30

            ws.write(row_num, col_num, row[col_num], style)

    wb.save(response)
    return response


class ExportPaymentStatus(View):
    """차수 및 타입별 수납 집계 현황"""

    def get(self, request):

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('차수_타입별_수납집계')

        worksheet.set_default_row(20)

        # ----------------- get_queryset start ----------------- #
        project = Project.objects.get(pk=request.GET.get('project'))
        date = request.GET.get('date')

        # Get some data to write to the spreadsheet.
        obj_list = ProjectIncBudget.objects.filter(project=project).order_by('order_group', 'unit_type')
        # ----------------- get_queryset finish ----------------- #

        rows_cnt = 9

        # 1. Title
        row_num = 0
        worksheet.set_row(row_num, 50)
        title_format = workbook.add_format()
        title_format.set_bold()
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        worksheet.merge_range(row_num, 0, row_num, rows_cnt, str(project) + ' 차수 및 타입별 수납 현황', title_format)

        # 2. Pre Header - Date
        row_num = 1
        worksheet.set_row(row_num, 18)
        worksheet.write(row_num, rows_cnt, date + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header
        row_num = 2
        worksheet.set_row(row_num, 25, workbook.add_format({'bold': True}))

        h_format = workbook.add_format()
        h_format.set_bold()
        h_format.set_border()
        h_format.set_align('center')
        h_format.set_align('vcenter')
        h_format.set_bg_color('#eeeeee')

        # Header_contents
        header_src = [['차수', 'order_group', 13],
                      ['타입', 'unit_type', 13],
                      ['단가(평균)', 'average_price', 15],
                      ['계획세대수', 'quantity', 11],
                      ['계약 현황', 'quantity', 11],
                      ['', 'quantity', 18],
                      ['', 'quantity', 18],
                      ['', 'quantity', 18],
                      ['', 'quantity', 18],
                      ['합계', 'budget', 18]]

        titles = []  # 헤더명
        params = []  # 헤더 컬럼(db)
        widths = []  # 헤더 넓이

        for ds in header_src:
            if ds:
                titles.append(ds[0])
                params.append(ds[1])
                widths.append(ds[2])

        # Adjust the column width.
        for i, col_width in enumerate(widths):  # 각 컬럼 넓이 세팅
            worksheet.set_column(i, i, col_width)

        # Write header
        for col_num, col in enumerate(titles):
            worksheet.write(row_num, col_num, titles[col_num], h_format)

        # Write header
        cont_col_num = (4, 5, 6, 7, 8)

        for col_num, col in enumerate(titles):  # 헤더 줄 제목 세팅
            if col == 4:
                worksheet.merge_range(row_num, col_num, row_num, col_num + 4, titles[col_num], h_format)
            elif int(col_num) not in cont_col_num:
                worksheet.merge_range(row_num, col_num, row_num + 1, col_num, titles[col_num], h_format)

        row_num = 3

        area_col1 = (4, 6) if project.is_returned_area else (4,)
        area_col2 = (5, 7) if project.is_returned_area else (5,)
        for col_num, col in enumerate(titles):
            if int(col_num) == 4:
                worksheet.write(row_num, col_num, '계약세대수', h_format)
            if int(col_num) == 5:
                worksheet.write(row_num, col_num, '계약금액', h_format)
            if int(col_num) == 6:
                worksheet.write(row_num, col_num, '실수납금액', h_format)
            if int(col_num) == 7:
                worksheet.write(row_num, col_num, '미수금액', h_format)
            if int(col_num) == 8:
                worksheet.write(row_num, col_num, '미계약금액', h_format)

        # 4. Body
        obj_list = obj_list.values_list(*params)

        b_format = workbook.add_format()
        b_format.set_border()
        b_format.set_align('right')
        b_format.set_align('vcenter')
        b_format.set_num_format('#,##0')

        body_format = {
            'border': True,
            'align': 'right',
            'valign': 'vcenter',
            'num_format': '#,##0'
        }

        # Write header
        for i, row in enumerate(obj_list):
            row = list(row)
            row_num += 1
            for col_num, cell_data in enumerate(row):
                if col_num == 0:
                    body_format['align'] = 'center'
                elif col_num == 1:
                    body_format['align'] = 'left'
                else:
                    body_format['align'] = 'right'
                bformat = workbook.add_format(body_format)
                worksheet.write(row_num, col_num, cell_data, bformat)

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = '{this_date}-payment-status.xlsx'.format(this_date=date)
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


class ExportProjectBalance(View):
    """프로젝트 계좌별 잔고 내역"""

    def get(self, request):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('계좌별_자금현황')

        worksheet.set_default_row(20)  # 기본 행 높이

        # data start --------------------------------------------- #

        project = Project.objects.get(pk=request.GET.get('project'))
        date = request.GET.get('date') if request.GET.get('date') else TODAY

        # 1. Title
        row_num = 0
        title_format = workbook.add_format()
        worksheet.set_row(row_num, 50)
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        title_format.set_bold()
        worksheet.write(row_num, 0, str(project) + ' 계좌별 자금현황', title_format)

        # 2. Header
        row_num = 1
        worksheet.set_row(row_num, 18)
        worksheet.write(row_num, 5, date + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header
        row_num = 2
        h_format = workbook.add_format()
        h_format.set_bold()
        h_format.set_border()
        h_format.set_align('center')
        h_format.set_align('vcenter')
        h_format.set_bg_color('#eeeeee')

        worksheet.set_column(0, 0, 10)
        worksheet.merge_range(row_num, 0, row_num, 1, '구분', h_format)
        worksheet.set_column(1, 1, 30)
        worksheet.set_column(2, 2, 20)
        worksheet.write(row_num, 2, '전일잔고', h_format)
        worksheet.set_column(3, 3, 20)
        worksheet.write(row_num, 3, '금일입금(증가)', h_format)
        worksheet.set_column(4, 4, 20)
        worksheet.write(row_num, 4, '금일출금(감소)', h_format)
        worksheet.set_column(5, 5, 20)
        worksheet.write(row_num, 5, '금일잔고', h_format)

        # 4. Contents
        b_format = workbook.add_format()
        b_format.set_valign('vcenter')
        b_format.set_border()
        b_format.set_num_format('#,##0')
        b_format.set_align('end')

        qs = ProjectCashBook.objects.all() \
            .order_by('bank_account') \
            .filter(is_separate=False,
                    bank_account__directpay=False,
                    deal_date__lte=date)

        balance_set = qs.annotate(bank_acc=F('bank_account__alias_name')) \
            .values('bank_acc') \
            .annotate(inc_sum=Sum('income'),
                      out_sum=Sum('outlay'),
                      date_inc=Sum(Case(
                          When(deal_date=date, then=F('income')),
                          default=0
                      )),
                      date_out=Sum(Case(
                          When(deal_date=date, then=F('outlay')),
                          default=0
                      )))

        total_inc = 0
        total_out = 0
        total_inc_sum = 0
        total_out_sum = 0

        for row, balance in enumerate(balance_set):
            row_num += 1
            inc_sum = balance['inc_sum'] if balance['inc_sum'] else 0
            out_sum = balance['out_sum'] if balance['out_sum'] else 0
            date_inc = balance['date_inc'] if balance['date_inc'] else 0
            date_out = balance['date_out'] if balance['date_out'] else 0

            total_inc += date_inc
            total_out += date_out
            total_inc_sum += inc_sum
            total_out_sum += out_sum

            for col in range(6):
                if col == 0 and row == 0:
                    worksheet.merge_range(row_num, col, balance_set.count() + 2, col, '보통예금', b_format)
                if col == 1:
                    worksheet.write(row_num, col, balance['bank_acc'], b_format)
                if col == 2:
                    worksheet.write(row_num, col, inc_sum - out_sum - date_inc + date_out, b_format)
                if col == 3:
                    worksheet.write(row_num, col, date_inc, b_format)
                if col == 4:
                    worksheet.write(row_num, col, date_out, b_format)
                if col == 5:
                    worksheet.write(row_num, col, inc_sum - out_sum, b_format)

        # 5. Sum row
        row_num += 1
        worksheet.merge_range(row_num, 0, row_num, 1, '현금성 자산 계', b_format)
        worksheet.write(row_num, 2, total_inc_sum - total_out_sum - total_inc + total_out, b_format)
        worksheet.write(row_num, 3, total_inc, b_format)
        worksheet.write(row_num, 4, total_out, b_format)
        worksheet.write(row_num, 5, total_inc_sum - total_out_sum, b_format)

        # data end ----------------------------------------------- #

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = f'{datetime.now().strftime("%Y-%m-%d")}-project-balance.xlsx'
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


class ExportProjectDateCashbook(View):
    """프로젝트 일별 입출금 내역"""

    def get(self, request):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('당일_입출금내역')

        worksheet.set_default_row(20)  # 기본 행 높이

        # data start --------------------------------------------- #

        project = Project.objects.get(pk=request.GET.get('project'))
        date = request.GET.get('date') if request.GET.get('date') else TODAY

        # 1. Title
        row_num = 0
        title_format = workbook.add_format()
        worksheet.set_row(row_num, 50)
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        title_format.set_bold()
        worksheet.write(row_num, 0, str(project) + ' 당일 입출금내역 [' + date + ' 기준]', title_format)

        # 2. Header
        row_num = 1
        worksheet.set_row(row_num, 18)
        # worksheet.write(row_num, 6, date + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header
        row_num = 2
        h_format = workbook.add_format()
        h_format.set_bold()
        h_format.set_border()
        h_format.set_align('center')
        h_format.set_align('vcenter')
        h_format.set_bg_color('#eeeeee')

        worksheet.set_column(0, 0, 15)
        worksheet.write(row_num, 0, '항목', h_format)
        worksheet.set_column(1, 1, 15)
        worksheet.write(row_num, 1, '세부항목', h_format)
        worksheet.set_column(2, 2, 20)
        worksheet.write(row_num, 2, '입금 금액', h_format)
        worksheet.set_column(3, 3, 20)
        worksheet.write(row_num, 3, '출금 금액', h_format)
        worksheet.set_column(4, 4, 25)
        worksheet.write(row_num, 4, '거래 계좌', h_format)
        worksheet.set_column(5, 5, 30)
        worksheet.write(row_num, 5, '거래처', h_format)
        worksheet.set_column(6, 6, 30)
        worksheet.write(row_num, 6, '적요', h_format)

        # 4. Contents
        b_format = workbook.add_format()
        b_format.set_valign('vcenter')
        b_format.set_border()
        b_format.set_num_format('#,##0')
        b_format.set_align('end')

        date_cashes = ProjectCashBook.objects.filter(is_separate=False, deal_date__exact=date).order_by('deal_date',
                                                                                                        'created_at',
                                                                                                        'id')

        inc_sum = 0
        out_sum = 0
        for row, cash in enumerate(date_cashes):
            row_num += 1
            inc_sum += cash.income if cash.income else 0
            out_sum += cash.outlay if cash.outlay else 0

            for col in range(7):
                if col == 0:
                    worksheet.write(row_num, col, cash.project_account_d1.name, b_format)
                if col == 1:
                    worksheet.write(row_num, col, cash.project_account_d2.name, b_format)
                if col == 2:
                    worksheet.write(row_num, col, cash.income, b_format)
                if col == 3:
                    worksheet.write(row_num, col, cash.outlay, b_format)
                if col == 4:
                    worksheet.write(row_num, col, cash.bank_account.alias_name, b_format)
                if col == 5:
                    worksheet.write(row_num, col, cash.trader, b_format)
                if col == 6:
                    worksheet.write(row_num, col, cash.content, b_format)

        # 5. Sum row
        row_num += 1
        worksheet.merge_range(row_num, 0, row_num, 1, '합계', b_format)
        worksheet.write(row_num, 2, inc_sum, b_format)
        worksheet.write(row_num, 3, out_sum, b_format)
        worksheet.write(row_num, 4, '', b_format)
        worksheet.write(row_num, 5, '', b_format)
        worksheet.write(row_num, 6, '', b_format)

        # data end ----------------------------------------------- #

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = f'{datetime.now().strftime("%Y-%m-%d")}-project-date-cashbook.xlsx'
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


class ExportBudgetExecutionStatus(View):
    """프로젝트 예산대비 현황"""

    def get(self, request):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('예산집행 현황')

        worksheet.set_default_row(20)  # 기본 행 높이

        # data start --------------------------------------------- #

        project = Project.objects.get(pk=request.GET.get('project'))
        date = request.GET.get('date')

        # 1. Title
        row_num = 0
        title_format = workbook.add_format()
        worksheet.set_row(row_num, 50)
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        title_format.set_bold()
        worksheet.write(row_num, 0, str(project) + ' 예산집행 현황', title_format)

        # 2. Header
        row_num = 1
        worksheet.set_row(row_num, 18)
        worksheet.write(row_num, 8, date + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header
        row_num = 2
        h_format = workbook.add_format()
        h_format.set_bold()
        h_format.set_border()
        h_format.set_align('center')
        h_format.set_align('vcenter')
        h_format.set_bg_color('#eeeeee')

        worksheet.set_column(0, 0, 10)
        worksheet.set_column(1, 1, 10)
        worksheet.set_column(2, 2, 12)
        worksheet.set_column(3, 3, 18)
        worksheet.merge_range(row_num, 0, row_num, 3, '구분', h_format)
        worksheet.set_column(4, 4, 20)
        worksheet.write(row_num, 4, '예산', h_format)
        worksheet.set_column(5, 5, 20)
        worksheet.write(row_num, 5, '전월 인출 금액 누계', h_format)
        worksheet.set_column(6, 6, 20)
        worksheet.write(row_num, 6, '당월 인출 금액', h_format)
        worksheet.set_column(7, 7, 20)
        worksheet.write(row_num, 7, '인출 금액 합계', h_format)
        worksheet.set_column(8, 8, 20)
        worksheet.write(row_num, 8, '가용 예산 합계', h_format)

        # 4. Contents
        b_format = workbook.add_format()
        b_format.set_valign('vcenter')
        b_format.set_border()
        b_format.set_num_format('#,##0')
        b_format.set_align('end')

        budget = ProjectOutBudget.objects.filter(project=project)
        rsp1 = budget.filter(account_d2__code__range=('322', '326')).count()  # 간접공사비
        rsp2 = budget.filter(account_d2__code__range=('327', '329')).count()  # 설계용역비
        rsp3 = budget.filter(account_d2__code__range=('331', '339')).count()  # 판매비
        rsp4 = budget.filter(account_d2__code__range=('341', '349')).count()  # 일반관리비
        rsp5 = budget.filter(account_d2__code__range=('351', '359')).count()  # 제세공과금
        budget_sum = budget.aggregate(Sum('budget'))['budget__sum']
        budget_month_sum = 0
        budget_total_sum = 0

        for row, bg in enumerate(budget):
            row_num += 1
            co_budget = ProjectCashBook.objects.filter(project=project,
                                                       project_account_d2=bg.account_d2,
                                                       deal_date__lte=date)

            co_budget_month = co_budget.filter(deal_date__gte=date[:8] + '01').aggregate(Sum('outlay'))['outlay__sum']
            co_budget_month = co_budget_month if co_budget_month else 0
            budget_month_sum += co_budget_month

            co_budget_total = co_budget.aggregate(Sum('outlay'))['outlay__sum']
            co_budget_total = co_budget_total if co_budget_total else 0
            budget_total_sum += co_budget_total

            for col in range(9):
                if col == 0 and row == 0:
                    worksheet.merge_range(row_num, col, budget.count() + 2, col, '사업비', b_format)
                if col == 1:
                    if int(bg.account_d2.code) == int(bg.account_d1.code) + 1:
                        worksheet.merge_range(row_num, col, row_num + bg.account_d1.projectoutbudget_set.count() - 1,
                                              col,
                                              bg.account_d1.name, b_format)
                if col == 2:
                    if bg.account_d2.sub_title:
                        crow = 5
                        if row == crow:
                            worksheet.merge_range(row_num, col, row_num + rsp1 - 1, col, bg.account_d2.sub_title,
                                                  b_format)
                        crow += rsp1
                        if row == crow:
                            worksheet.merge_range(row_num, col, row_num + rsp2 - 1, col, bg.account_d2.sub_title,
                                                  b_format)
                        crow = crow + rsp2 + rsp3
                        if row == crow:
                            worksheet.merge_range(row_num, col, row_num + rsp4 - 1, col, bg.account_d2.sub_title,
                                                  b_format)
                        crow += rsp4
                        if row == crow:
                            worksheet.merge_range(row_num, col, row_num + rsp5 - 1, col, bg.account_d2.sub_title,
                                                  b_format)
                    else:
                        worksheet.merge_range(row_num, col, row_num, col + 1, bg.account_d2.name, b_format)
                if col == 3:
                    if bg.account_d2.sub_title:
                        worksheet.write(row_num, col, bg.account_d2.name, b_format)
                if col == 4:
                    worksheet.write(row_num, col, bg.budget, b_format)
                if col == 5:
                    worksheet.write(row_num, col, co_budget_total - co_budget_month, b_format)
                if col == 6:
                    worksheet.write(row_num, col, co_budget_month, b_format)
                if col == 7:
                    worksheet.write(row_num, col, co_budget_total, b_format)
                if col == 8:
                    worksheet.write(row_num, col, bg.budget - co_budget_total, b_format)

        # 5. Sum row
        row_num += 1
        worksheet.merge_range(row_num, 0, row_num, 3, '합 계', b_format)
        worksheet.write(row_num, 4, budget_sum, b_format)
        worksheet.write(row_num, 5, budget_total_sum - budget_month_sum, b_format)
        worksheet.write(row_num, 6, budget_month_sum, b_format)
        worksheet.write(row_num, 7, budget_total_sum, b_format)
        worksheet.write(row_num, 8, budget_sum - budget_total_sum, b_format)

        # data end ----------------------------------------------- #

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = f'{datetime.now().strftime("%Y-%m-%d")}-budget_status.xlsx'
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


def export_project_cash_xls(request):
    """프로젝트별 입출금 내역"""
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename={date}-project-cashbook.xls'.format(
        date=datetime.now().strftime('%Y-%m-%d'))

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('프로젝트_입출금_내역')  # 시트 이름

    # get_data: ?project=1&sdate=2020-12-01&edate=2020-12-31&sort=1&d1=1&d2=1&bank_acc=5&q=ㅁ
    project = Project.objects.get(pk=request.GET.get('project'))
    sdate = request.GET.get('sdate')
    edate = request.GET.get('edate')
    sort = request.GET.get('sort')
    d1 = request.GET.get('d1')
    d2 = request.GET.get('d2')
    bank_acc = request.GET.get('bank_acc')
    q = request.GET.get('q')

    today = TODAY
    sdate = sdate if sdate else '1900-01-01'
    edate = edate if edate else today
    obj_list = ProjectCashBook.objects.filter(project=project, deal_date__range=(sdate, edate)).order_by('-deal_date',
                                                                                                         '-created_at')
    is_imp = request.GET.get('imp')
    obj_list = obj_list.filter(is_imprest=True) if is_imp == '1' else obj_list.filter(is_imprest=False)

    if sort:
        obj_list = obj_list.filter(sort_id=sort)

    if d1:
        obj_list = obj_list.filter(project_account_d1_id=d1)

    if d2:
        obj_list = obj_list.filter(project_account_d2_id=d2)

    if bank_acc:
        obj_list = obj_list.filter(bank_account_id=bank_acc)

    if q:
        obj_list = obj_list.filter(Q(content__icontains=q) | Q(trader__icontains=q))

    # Sheet Title, first row
    row_num = 0

    style = xlwt.XFStyle()
    style.font.bold = True
    style.font.height = 300
    style.alignment.vert = style.alignment.VERT_CENTER  # 수직정렬

    ws.write(row_num, 0, str(project) + ' 입출금 내역', style)
    ws.row(0).height_mismatch = True
    ws.row(0).height = 38 * 20

    # title_list

    resources = [
        ['거래일자', 'deal_date'],
        ['구분', 'sort__name'],
        ['현장 계정', 'project_account_d1__name'],
        ['현장 세부계정', 'project_account_d2__name'],
        ['적요', 'content'],
        ['거래처', 'trader'],
        ['거래 계좌', 'bank_account__alias_name'],
        ['입금 금액', 'income'],
        ['출금 금액', 'outlay'],
        ['비고', 'note']]

    columns = []
    params = []

    for rsc in resources:
        columns.append(rsc[0])
        params.append(rsc[1])

    rows = obj_list.values_list(*params)

    # Sheet header, second row
    row_num = 1

    style = xlwt.XFStyle()
    style.font.bold = True

    # 테두리 설정
    # 가는 실선 : 1, 작은 굵은 실선 : 2,가는 파선 : 3, 중간가는 파선 : 4, 큰 굵은 실선 : 5, 이중선 : 6,가는 점선 : 7
    # 큰 굵은 점선 : 8,가는 점선 : 9, 굵은 점선 : 10,가는 이중 점선 : 11, 굵은 이중 점선 : 12, 사선 점선 : 13
    style.borders.left = 1
    style.borders.right = 1
    style.borders.top = 1
    style.borders.bottom = 1

    style.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    style.pattern.pattern_fore_colour = xlwt.Style.colour_map['silver_ega']

    style.alignment.vert = style.alignment.VERT_CENTER  # 수직정렬
    style.alignment.horz = style.alignment.HORZ_CENTER  # 수평정렬

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style)

    # Sheet body, remaining rows
    style = xlwt.XFStyle()
    # 테두리 설정
    style.borders.left = 1
    style.borders.right = 1
    style.borders.top = 1
    style.borders.bottom = 1

    style.alignment.vert = style.alignment.VERT_CENTER  # 수직정렬
    # style.alignment.horz = style.alignment.HORZ_CENTER  # 수평정렬

    for row in rows:
        row_num += 1
        for col_num, col in enumerate((columns)):
            row = list(row)

            if col == '거래일자':
                style.num_format_str = 'yyyy-mm-dd'
                ws.col(col_num).width = 110 * 30

            if col == '구분':
                if row[col_num] == '1':
                    row[col_num] = '입금'
                if row[col_num] == '2':
                    row[col_num] = '출금'
                if row[col_num] == '3':
                    row[col_num] = '대체'

            if col == '현장 계정':
                ws.col(col_num).width = 110 * 30

            if col == '현장 세부계정':
                ws.col(col_num).width = 160 * 30

            if col == '적요' or col == '거래처':
                ws.col(col_num).width = 180 * 30

            if col == '거래 계좌':
                ws.col(col_num).width = 170 * 30

            if '금액' in col:
                style.num_format_str = '#,##'
                ws.col(col_num).width = 110 * 30

            if col == '비고':
                ws.col(col_num).width = 256 * 30

            ws.write(row_num, col_num, row[col_num], style)

    wb.save(response)
    return response


class ExportSites(View):
    """프로젝트 지번별 토지목록"""

    @staticmethod
    def get(request):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('지번별_토지목록')

        worksheet.set_default_row(20)  # 기본 행 높이

        # data start --------------------------------------------- #

        # -------------------- get_queryset start -------------------- #
        project = Project.objects.get(pk=request.GET.get('project'))
        obj_list = Site.objects.filter(project=project).order_by('order')
        # -------------------- get_queryset finish -------------------- #

        rows_cnt = 7

        # 1. Title
        row_num = 0
        worksheet.set_row(row_num, 50)

        title_format = workbook.add_format()
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        title_format.set_bold()
        worksheet.merge_range(row_num, 0, row_num, rows_cnt, str(project) + ' 토지목록 조서', title_format)

        # 2. Pre Header - Date
        row_num = 1
        worksheet.set_row(row_num, 18)
        worksheet.write(row_num, rows_cnt, TODAY + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header
        row_num = 2
        worksheet.set_row(row_num, 25, workbook.add_format({'bold': True}))

        header_format = workbook.add_format()
        header_format.set_bold()
        header_format.set_border()
        header_format.set_align('center')
        header_format.set_align('vcenter')
        header_format.set_bg_color('#eeeeee')

        # Header_contents
        at = '소유면적'
        area_title = at + '(환지면적 기준)' if project.is_returned_area else at
        header_src = [
            ['No', 'order', 10],
            ['행정동', 'district', 15],
            ['지번', 'lot_number', 15],
            ['지목', 'site_purpose', 12],
            ['대지면적', 'official_area', 13],
            ['', '', 13],
        ]

        if project.is_returned_area:
            header_src.append(['환지면적', 'returned_area', 13])
            header_src.append(['', '', 13])

        titles = []  # 헤더명
        params = []  # 헤더 컬럼(db)
        widths = []  # 헤더 넓이

        for src in header_src:  # 요청된 컬럼 개수 만큼 반복 (1-2-3... -> i)
            titles.append(src[0])  # 헤더명
            params.append(src[1])  # 헤더 컬럼(db)
            widths.append(src[2])  # 헤더 넓이

        # Adjust the column width.
        for i, cw in enumerate(widths):  # 각 컬럼 넙이 세팅
            worksheet.set_column(i, i, cw)

        # Write header
        area_col_num = (4, 5, 6, 7) if project.is_returned_area else (4, 5)

        for col_num, col in enumerate(titles):  # 헤더 줄 제목 세팅
            if '면적' in col:
                worksheet.merge_range(row_num, col_num, row_num, col_num + 1, titles[col_num], header_format)
            elif int(col_num) not in area_col_num:
                worksheet.merge_range(row_num, col_num, row_num + 1, col_num, titles[col_num], header_format)

        row_num = 3

        area_col1 = (4, 6) if project.is_returned_area else (4,)
        area_col2 = (5, 7) if project.is_returned_area else (5,)
        for col_num, col in enumerate(titles):
            if int(col_num) in area_col1:
                worksheet.write(row_num, col_num, '㎡', header_format)
            elif int(col_num) in area_col2:
                worksheet.write(row_num, col_num, '평', header_format)

        #################################################################
        # 4. Body
        # Get some data to write to the spreadsheet.

        # data = obj_list.values_list(*params)

        body_format = {
            'border': True,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '#,##0.00',
        }

        while '' in params:
            params.remove('')

        rows = obj_list.values_list(*params)

        for row in rows:
            row_num += 1
            for col_num, cell_data in enumerate(titles):
                row = list(row)

                # if col_num in (2, 8):
                #     body_format['num_format'] = 'yyyy-mm-dd'

                if col_num in area_col_num:
                    body_format['align'] = 'right'
                    body_format['num_format'] = '#,##0.00'
                else:
                    body_format['align'] = 'center'
                    body_format['num_format'] = '#,##0'

                bf = workbook.add_format(body_format)

                if col_num == 5:
                    worksheet.write(row_num, col_num, float(row[col_num - 1]) * 0.3025, bf)
                elif col_num == 7:
                    worksheet.write(row_num, col_num, float(row[col_num - 2]) * 0.3025, bf)

                if col_num < 5:
                    worksheet.write(row_num, col_num, row[col_num], bf)
                elif col_num < 7:
                    worksheet.write(row_num, col_num, row[col_num - 1], bf)
                else:
                    worksheet.write(row_num, col_num, row[col_num - 2], bf)
        #################################################################

        # data finish -------------------------------------------- #

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = f'{datetime.now().strftime("%Y-%m-%d")}-sites.xlsx'
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


class ExportSitesByOwner(View):
    """프로젝트 소유자별 토지목록"""

    def get(self, request):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('소유자별_토지목록')

        worksheet.set_default_row(20)  # 기본 행 높이

        # data start --------------------------------------------- #

        ##### ----------------- get_queryset start ----------------- #####
        project = Project.objects.get(pk=request.GET.get('project'))
        obj_list = SiteOwner.objects.filter(project=project).order_by('owner', 'id')
        ##### ----------------- get_queryset finish ----------------- #####

        rows_cnt = 8

        # 1. Title
        row_num = 0
        worksheet.set_row(row_num, 50)

        title_format = workbook.add_format()
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        title_format.set_bold()
        worksheet.merge_range(row_num, 0, row_num, rows_cnt, str(project) + ' 소유자목록 조서', title_format)

        # 2. Pre Header - Date
        row_num = 1
        worksheet.set_row(row_num, 18)
        worksheet.write(row_num, rows_cnt, TODAY + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header
        row_num = 2
        worksheet.set_row(row_num, 25, workbook.add_format({'bold': True}))

        header_format = workbook.add_format()
        header_format.set_bold()
        header_format.set_border()
        header_format.set_align('center')
        header_format.set_align('vcenter')
        header_format.set_bg_color('#eeeeee')

        # Header_contents
        at = '소유면적'
        area_title = at + '(환지면적 기준)' if project.is_returned_area else at
        header_src = [
            ['소유구분', 'own_sort', 10],
            ['소유자', 'owner', 15],
            ['생년월일', 'date_of_birth', 15],
            ['주연락처', 'phone1', 18],
            ['소유부지(지번)', 'sites__lot_number', 12],
            ['소유지분(%)', 'relations__ownership_ratio', 10],
            [area_title, 'relations__owned_area', 12],
            ['', '', 12],
            ['소유권 취득일', 'relations__acquisition_date', 15]
        ]

        titles = []  # 헤더명
        params = []  # 헤더 컬럼(db)
        widths = []  # 헤더 넓이

        for src in header_src:  # 요청된 컬럼 개수 만큼 반복 (1-2-3... -> i)
            titles.append(src[0])  # 일련번호
            params.append(src[1])  # serial_number
            widths.append(src[2])  # 10

        # Adjust the column width.
        for i, cw in enumerate(widths):  # 각 컬럼 넙이 세팅
            worksheet.set_column(i, i, cw)

        # Write header
        for col_num, col in enumerate(titles):  # 헤더 줄 제목 세팅
            if '면적' in col:
                worksheet.merge_range(row_num, col_num, row_num, col_num + 1, titles[col_num], header_format)
            elif int(col_num) not in (6, 7):
                worksheet.merge_range(row_num, col_num, row_num + 1, col_num, titles[col_num], header_format)

        row_num = 3

        for col_num, col in enumerate(titles):
            if int(col_num) == 6:
                worksheet.write(row_num, col_num, '㎡', header_format)
            elif int(col_num) == 7:
                worksheet.write(row_num, col_num, '평', header_format)

        #################################################################
        # 4. Body
        # Get some data to write to the spreadsheet.

        # data = obj_list.values_list(*params)

        body_format = {
            'border': True,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '#,##0.00',
        }

        while '' in params:
            params.remove('')

        rows = obj_list.values_list(*params)

        for row in rows:
            row_num += 1
            for col_num, cell_data in enumerate(titles):
                row = list(row)

                if col_num in (2, 8):
                    body_format['num_format'] = 'yyyy-mm-dd'

                if col_num in (5, 6, 7):
                    body_format['align'] = 'right'
                    body_format['num_format'] = '#,##0.00'
                else:
                    body_format['align'] = 'center'

                bf = workbook.add_format(body_format)

                if col_num == 0:
                    worksheet.write(row_num, col_num, self.get_sort(row[col_num]), bf)
                elif col_num == 7:
                    worksheet.write(row_num, col_num, float(row[col_num - 1]) * 0.3025, bf)
                else:
                    if col_num < 8:
                        worksheet.write(row_num, col_num, row[col_num], bf)
                    else:
                        worksheet.write(row_num, col_num, row[col_num - 1], bf)
        #################################################################

        # data finish -------------------------------------------- #

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = f'{datetime.now().strftime("%Y-%m-%d")}-sites-by-owner.xlsx'
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    def get_sort(self, code):
        sort = ('', '개인', '법인', '국공유지')
        return sort[int(code)]


class ExportSitesContracts(View):
    """프로젝트 토지 계약현황"""

    def get(self, request):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('사업부지_계약현황')

        worksheet.set_default_row(20)  # 기본 행 높이

        # data start --------------------------------------------- #

        ##### ----------------- get_queryset start ----------------- #####
        project = Project.objects.get(pk=request.GET.get('project'))
        obj_list = SiteContract.objects.filter(project=project).order_by('contract_date', 'id')
        ##### ----------------- get_queryset finish ----------------- #####

        rows_cnt = 12

        # 1. Title
        row_num = 0
        worksheet.set_row(row_num, 50)

        title_format = workbook.add_format()
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        title_format.set_bold()
        worksheet.merge_range(row_num, 0, row_num, rows_cnt, str(project) + ' 사업부지 계약현황', title_format)

        # 2. Pre Header - Date
        row_num = 1
        worksheet.set_row(row_num, 18)
        worksheet.write(row_num, rows_cnt, TODAY + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header
        row_num = 2
        worksheet.set_row(row_num, 25, workbook.add_format({'bold': True}))

        header_format = workbook.add_format()
        header_format.set_bold()
        header_format.set_border()
        header_format.set_align('center')
        header_format.set_align('vcenter')
        header_format.set_bg_color('#eeeeee')

        # Header_contents
        header_src = [['소유구분', 'owner__own_sort', 8],
                      ['소유자', 'owner__owner', 12],
                      ['계약일', 'contract_date', 15],
                      ['총 계약면적', 'contract_area', 8],
                      ['', '', 8],
                      ['총 매매대금', 'total_price', 15],
                      ['계약금1', 'down_pay1', 12],
                      ['지급여부', 'down_pay1_is_paid', 8],
                      ['계약금2', 'down_pay2', 12],
                      ['중도금', 'inter_pay1', 12],
                      ['잔금', 'remain_pay', 15],
                      ['지급여부', 'remain_pay_is_paid', 8],
                      ['비고', 'note', 25]]

        titles = []  # 헤더명
        params = []  # 헤더 컬럼(db)
        widths = []  # 헤더 넓이

        for src in header_src:  # 요청된 컬럼 개수 만큼 반복 (1-2-3... -> i)
            titles.append(src[0])  # 일련번호
            params.append(src[1])  # serial_number
            widths.append(src[2])  # 10

        # Adjust the column width.
        for i, cw in enumerate(widths):  # 각 컬럼 넙이 세팅
            worksheet.set_column(i, i, cw)

        # Write header
        for col_num, col in enumerate(titles):  # 헤더 줄 제목 세팅
            if '면적' in col:
                worksheet.merge_range(row_num, col_num, row_num, col_num + 1, titles[col_num], header_format)
            elif int(col_num) not in (3, 4):
                worksheet.merge_range(row_num, col_num, row_num + 1, col_num, titles[col_num], header_format)

        row_num = 3

        for col_num, col in enumerate(titles):
            if int(col_num) == 3:
                worksheet.write(row_num, col_num, '㎡', header_format)
            elif int(col_num) == 4:
                worksheet.write(row_num, col_num, '평', header_format)

        #################################################################
        # 4. Body
        # Get some data to write to the spreadsheet.

        # data = obj_list.values_list(*params)

        body_format = {
            'border': True,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': 'yyyy-mm-dd',
        }

        while '' in params:
            params.remove('')

        rows = obj_list.values_list(*params)

        for row in rows:
            row_num += 1
            for col_num, cell_data in enumerate(titles):
                row = list(row)

                if col_num == 2:
                    body_format['num_format'] = 'yyyy-mm-dd'
                elif col_num in (3, 4):
                    body_format['num_format'] = '#,##0.00'
                else:
                    body_format['num_format'] = '#,##0'

                bf = workbook.add_format(body_format)

                if col_num == 0:
                    worksheet.write(row_num, col_num, self.get_sort(row[col_num]), bf)
                elif col_num == 4:
                    worksheet.write(row_num, col_num, float(row[col_num - 1]) * 0.3025, bf)
                else:
                    if col_num < 5:
                        worksheet.write(row_num, col_num, self.get_row_content(row[col_num]), bf)
                    else:
                        worksheet.write(row_num, col_num, self.get_row_content(row[col_num - 1]), bf)
        #################################################################

        # data end ----------------------------------------------- #

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = f'{datetime.now().strftime("%Y-%m-%d")}-sites-contracts.xlsx'
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    def get_sort(self, code):
        sort = ('', '개인', '법인', '국공유지')
        return sort[int(code)]

    def get_row_content(self, cont):
        if cont == True:
            return '완료'
        elif cont == False:
            return ''
        else:
            return cont


class ExportBalanceByAcc(View):
    """본사 계좌별 잔고 내역"""

    def get(self, request):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('본사_계좌별_자금현황')

        worksheet.set_default_row(20)  # 기본 행 높이

        # data start --------------------------------------------- #

        company = Company.objects.first()
        date = request.GET.get('date') if request.GET.get('date') else TODAY

        # 1. Title
        row_num = 0
        title_format = workbook.add_format()
        worksheet.set_row(row_num, 50)
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        title_format.set_bold()
        worksheet.write(row_num, 0, str(company) + ' 계좌별 자금현황', title_format)

        # 2. Header
        row_num = 1
        worksheet.set_row(row_num, 18)
        worksheet.write(row_num, 5, date + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header
        row_num = 2
        h_format = workbook.add_format()
        h_format.set_bold()
        h_format.set_border()
        h_format.set_align('center')
        h_format.set_align('vcenter')
        h_format.set_bg_color('#eeeeee')

        worksheet.set_column(0, 0, 10)
        worksheet.merge_range(row_num, 0, row_num, 1, '구분', h_format)
        worksheet.set_column(1, 1, 30)
        worksheet.set_column(2, 2, 20)
        worksheet.write(row_num, 2, '전일잔고', h_format)
        worksheet.set_column(3, 3, 20)
        worksheet.write(row_num, 3, '금알입금(증가)', h_format)
        worksheet.set_column(4, 4, 20)
        worksheet.write(row_num, 4, '금일출금(감소)', h_format)
        worksheet.set_column(5, 5, 20)
        worksheet.write(row_num, 5, '금일잔고', h_format)

        # 4. Contents
        b_format = workbook.add_format()
        b_format.set_valign('vcenter')
        b_format.set_border()
        b_format.set_num_format('#,##0')
        b_format.set_align('end')

        qs = CashBook.objects.all() \
            .order_by('bank_account') \
            .filter(is_separate=False, deal_date__lte=date)

        balance_set = qs.annotate(bank_acc=F('bank_account__alias_name')) \
            .values('bank_acc') \
            .annotate(inc_sum=Sum('income'),
                      out_sum=Sum('outlay'),
                      date_inc=Sum(Case(
                          When(deal_date=date, then=F('income')),
                          default=0
                      )),
                      date_out=Sum(Case(
                          When(deal_date=date, then=F('outlay')),
                          default=0
                      )))

        total_inc = 0
        total_out = 0
        total_inc_sum = 0
        total_out_sum = 0

        for row, balance in enumerate(balance_set):
            row_num += 1
            inc_sum = balance['inc_sum'] if balance['inc_sum'] else 0
            out_sum = balance['out_sum'] if balance['out_sum'] else 0
            date_inc = balance['date_inc'] if balance['date_inc'] else 0
            date_out = balance['date_out'] if balance['date_out'] else 0

            total_inc += date_inc
            total_out += date_out
            total_inc_sum += inc_sum
            total_out_sum += out_sum

            for col in range(6):
                if col == 0 and row == 0:
                    worksheet.write(row_num, col, '현금', b_format)
                if col == 0 and row == 1:
                    worksheet.merge_range(row_num, col, balance_set.count() + 2, col, '보통예금', b_format)
                if col == 1:
                    worksheet.write(row_num, col, balance['bank_acc'], b_format)
                if col == 2:
                    worksheet.write(row_num, col, inc_sum - out_sum - date_inc + date_out, b_format)
                if col == 3:
                    worksheet.write(row_num, col, date_inc, b_format)
                if col == 4:
                    worksheet.write(row_num, col, date_out, b_format)
                if col == 5:
                    worksheet.write(row_num, col, inc_sum - out_sum, b_format)

        # 5. Sum row
        row_num += 1
        worksheet.merge_range(row_num, 0, row_num, 1, '현금성 자산 계', b_format)
        worksheet.write(row_num, 2, total_inc_sum - total_out_sum - total_inc + total_out, b_format)
        worksheet.write(row_num, 3, total_inc, b_format)
        worksheet.write(row_num, 4, total_out, b_format)
        worksheet.write(row_num, 5, total_inc_sum - total_out_sum, b_format)

        # data end ----------------------------------------------- #

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = f'{datetime.now().strftime("%Y-%m-%d")}-project-balance.xlsx'
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


class ExportDateCashbook(View):
    """본사 일별 입출금 내역"""

    def get(self, request):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('당일_입출금내역')

        worksheet.set_default_row(20)  # 기본 행 높이

        # data start --------------------------------------------- #

        company = Company.objects.first()
        date = request.GET.get('date') if request.GET.get('date') else TODAY

        # 1. Title
        row_num = 0
        title_format = workbook.add_format()
        worksheet.set_row(row_num, 50)
        title_format.set_font_size(18)
        title_format.set_align('vcenter')
        title_format.set_bold()
        worksheet.write(row_num, 0, str(company) + ' 당일 입출금내역 [' + date + ' 기준]', title_format)

        # 2. Header
        row_num = 1
        worksheet.set_row(row_num, 18)
        # worksheet.write(row_num, 7, date + ' 현재', workbook.add_format({'align': 'right'}))

        # 3. Header
        row_num = 2
        h_format = workbook.add_format()
        h_format.set_bold()
        h_format.set_border()
        h_format.set_align('center')
        h_format.set_align('vcenter')
        h_format.set_bg_color('#eeeeee')

        worksheet.set_column(0, 0, 15)
        worksheet.write(row_num, 0, '구분', h_format)
        worksheet.set_column(1, 1, 15)
        worksheet.write(row_num, 1, '항목', h_format)
        worksheet.set_column(2, 2, 15)
        worksheet.write(row_num, 2, '세부항목', h_format)
        worksheet.set_column(3, 3, 20)
        worksheet.write(row_num, 3, '입금 금액', h_format)
        worksheet.set_column(4, 4, 20)
        worksheet.write(row_num, 4, '출금 금액', h_format)
        worksheet.set_column(5, 5, 25)
        worksheet.write(row_num, 5, '거래 계좌', h_format)
        worksheet.set_column(6, 6, 30)
        worksheet.write(row_num, 6, '거래처', h_format)
        worksheet.set_column(7, 7, 30)
        worksheet.write(row_num, 7, '적요', h_format)

        # 4. Contents
        b_format = workbook.add_format()
        b_format.set_valign('vcenter')
        b_format.set_border()
        b_format.set_num_format('#,##0')
        b_format.set_align('end')

        date_cashes = CashBook.objects.filter(is_separate=False, deal_date__exact=date).order_by('deal_date',
                                                                                                 'created_at',
                                                                                                 'id')

        inc_sum = 0
        out_sum = 0
        for row, cash in enumerate(date_cashes):
            row_num += 1
            inc_sum += cash.income if cash.income else 0
            out_sum += cash.outlay if cash.outlay else 0

            for col in range(8):
                if col == 0:
                    worksheet.write(row_num, col, cash.sort.name + '-' + cash.account_d1.name, b_format)
                if col == 1:
                    worksheet.write(row_num, col, cash.account_d2.name, b_format)
                if col == 2:
                    worksheet.write(row_num, col, cash.account_d3.name, b_format)
                if col == 3:
                    worksheet.write(row_num, col, cash.income, b_format)
                if col == 4:
                    worksheet.write(row_num, col, cash.outlay, b_format)
                if col == 5:
                    worksheet.write(row_num, col, cash.bank_account.alias_name, b_format)
                if col == 6:
                    worksheet.write(row_num, col, cash.trader, b_format)
                if col == 7:
                    worksheet.write(row_num, col, cash.content, b_format)

        # 5. Sum row
        row_num += 1
        worksheet.merge_range(row_num, 0, row_num, 1, '합계', b_format)
        worksheet.write(row_num, 2, '', b_format)
        worksheet.write(row_num, 3, inc_sum, b_format)
        worksheet.write(row_num, 4, out_sum, b_format)
        worksheet.write(row_num, 5, '', b_format)
        worksheet.write(row_num, 6, '', b_format)
        worksheet.write(row_num, 7, '', b_format)

        # data end ----------------------------------------------- #

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = f'{datetime.now().strftime("%Y-%m-%d")}-project-date-cashbook.xlsx'
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


def export_cashbook_xls(request):
    """본사 입출금 내역"""
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename={date}-cashbook.xls'.format(
        date=datetime.now().strftime('%Y-%m-%d'))

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('본사_입출금_내역')  # 시트 이름

    # get_data: ?s_date=2018-06-30&e_date=&category1=&category2=&bank_account=&search_word=
    s_date = request.GET.get('s_date')
    e_date = request.GET.get('e_date')
    sort = request.GET.get('sort')
    account_d1 = request.GET.get('account_d1')
    account_d2 = request.GET.get('account_d2')
    account_d3 = request.GET.get('account_d3')
    bank_account = request.GET.get('bank_account')
    search_word = request.GET.get('search_word')

    company = Company.objects.first()
    today = TODAY
    s_date = s_date if s_date else '1900-01-01'
    e_date = e_date if e_date else today

    obj_list = CashBook.objects.filter(company=company, deal_date__range=(s_date, e_date))

    if sort:
        obj_list = obj_list.filter(sort_id=sort)

    if account_d1:
        obj_list = obj_list.filter(account_d1_id=account_d1)

    if account_d2:
        obj_list = obj_list.filter(account_d2_id=account_d2)

    if account_d3:
        obj_list = obj_list.filter(account_d3_id=account_d3)

    if bank_account:
        obj_list = obj_list.filter(bank_account_id=bank_account)

    if search_word:
        obj_list = obj_list.filter(
            Q(content__icontains=search_word) |
            Q(trader__icontains=search_word) |
            Q(note__icontains=search_word))

    # Sheet Title, first row
    row_num = 0

    style = xlwt.XFStyle()
    style.font.bold = True
    style.font.height = 300
    style.alignment.vert = style.alignment.VERT_CENTER  # 수직정렬

    ws.write(row_num, 0, str(company) + ' 입출금 내역', style)
    ws.row(0).height_mismatch = True
    ws.row(0).height = 38 * 20

    # title_list

    resources = [
        ['거래일자', 'deal_date'],
        ['구분', 'sort__name'],
        ['계정', 'account_d1__name'],
        ['중분류', 'account_d2__name'],
        ['세부계정', 'account_d3__name'],
        ['적요', 'content'],
        ['거래처', 'trader'],
        ['거래계좌', 'bank_account__alias_name'],
        ['입금금액', 'income'],
        ['출금금액', 'outlay'],
        ['비고', 'note']]

    columns = []
    params = []

    for rsc in resources:
        columns.append(rsc[0])
        params.append(rsc[1])

    rows = obj_list.values_list(*params)

    # Sheet header, second row
    row_num = 1

    style = xlwt.XFStyle()
    style.font.bold = True

    # 테두리 설정
    # 가는 실선 : 1, 작은 굵은 실선 : 2,가는 파선 : 3, 중간가는 파선 : 4, 큰 굵은 실선 : 5, 이중선 : 6,가는 점선 : 7
    # 큰 굵은 점선 : 8,가는 점선 : 9, 굵은 점선 : 10,가는 이중 점선 : 11, 굵은 이중 점선 : 12, 사선 점선 : 13
    style.borders.left = 1
    style.borders.right = 1
    style.borders.top = 1
    style.borders.bottom = 1

    style.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    style.pattern.pattern_fore_colour = xlwt.Style.colour_map['silver_ega']

    style.alignment.vert = style.alignment.VERT_CENTER  # 수직정렬
    style.alignment.horz = style.alignment.HORZ_CENTER  # 수평정렬

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style)

    # Sheet body, remaining rows
    style = xlwt.XFStyle()
    # 테두리 설정
    style.borders.left = 1
    style.borders.right = 1
    style.borders.top = 1
    style.borders.bottom = 1

    style.alignment.vert = style.alignment.VERT_CENTER  # 수직정렬
    # style.alignment.horz = style.alignment.HORZ_CENTER  # 수평정렬

    for row in rows:
        row_num += 1
        for col_num, col in enumerate((columns)):
            row = list(row)

            if col == '거래일자':
                style.num_format_str = 'yyyy-mm-dd'
                ws.col(col_num).width = 110 * 30

            if col == '구분':
                if row[col_num] == '1':
                    row[col_num] = '입금'
                if row[col_num] == '2':
                    row[col_num] = '출금'
                if row[col_num] == '3':
                    row[col_num] = '대체'

            if col == '계정':
                if row[col_num] == '1':
                    row[col_num] = '자산'
                if row[col_num] == '2':
                    row[col_num] = '부채'
                if row[col_num] == '3':
                    row[col_num] = '자본'
                if row[col_num] == '4':
                    row[col_num] = '수익'
                if row[col_num] == '5':
                    row[col_num] = '비용'
                if row[col_num] == '6':
                    row[col_num] = '대체'

            if col == '현장 계정':
                ws.col(col_num).width = 110 * 30

            if col == '세부계정':
                ws.col(col_num).width = 160 * 30

            if col == '적요' or col == '거래처':
                ws.col(col_num).width = 180 * 30

            if col == '거래계좌':
                ws.col(col_num).width = 170 * 30

            if '금액' in col:
                style.num_format_str = '#,##'
                ws.col(col_num).width = 110 * 30

            if col == '증빙자료':
                if row[col_num] == '0':
                    row[col_num] = '증빙 없음'
                if row[col_num] == '1':
                    row[col_num] = '세금계산서'
                if row[col_num] == '2':
                    row[col_num] = '계산서(면세)'
                if row[col_num] == '3':
                    row[col_num] = '신용카드전표'
                if row[col_num] == '4':
                    row[col_num] = '현금영수증'
                if row[col_num] == '5':
                    row[col_num] = '간이영수증'
                ws.col(col_num).width = 100 * 30

            if col == '비고':
                ws.col(col_num).width = 256 * 30

            ws.write(row_num, col_num, row[col_num], style)

    wb.save(response)
    return response


class ExportExamples(View):
    """Examples"""

    def get(self, request):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('시트 타이틀')

        worksheet.set_default_row(20)  # 기본 행 높이

        # data start --------------------------------------------- #

        # data finish -------------------------------------------- #

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = f'{datetime.now().strftime("%Y-%m-%d")}-file_title.xlsx'
        file_format = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(output, content_type=file_format)
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
