class RegularUnitView(HttpBaseView):
    url_path = "regularunit"
    methods = ["search","cm_func","d_import"
               ,"d_export","m_export"]
    
    #获得单位维护数据
    def search(self, request, download=False):
        pass
    
    #获得单位维护数据导出
    def d_export(self, request):
        pass
    
    #模板导出
    def m_export(self, request):
        pass
        
    #数据导入
    def d_import(self, request):
        pass
    
    #新增/编辑规范单位
    def cm_func(self, request):
        pass