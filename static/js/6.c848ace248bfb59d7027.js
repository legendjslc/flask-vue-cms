webpackJsonp([6],{"0Syk":function(t,e,a){"use strict";e.b=function(){return Object(s.a)({url:"/sysinfo",method:"get"})},e.c=function(t){return Object(s.a)({url:"/operation_log",method:"get",params:t})},e.a=function(t){return Object(s.a)({url:"/operation_log/delete",method:"delete",data:t})};var s=a("vLgD")},ARoL:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var s=a("0Syk"),n={name:"dashboard",data:function(){return{cpu:{},sys:{},mem:{},listLoading:!0,mem_avaliable:0,mem_used:0,mem_free:0,disk:null,user:null}},created:function(){this.getInfo()},filters:{sizeformat:function(t){return parseFloat(t/1073741824).toFixed(2)}},methods:{getInfo:function(){var t=this;this.listLoading=!0,Object(s.b)().then(function(e){t.listLoading=!1,t.cpu=e.data.cpu,t.sys=e.data.sys,t.mem=e.data.mem,t.mem_avaliable=Math.round(t.mem.available/t.mem.total*100),t.mem_used=Math.round(t.mem.used/t.mem.total*100),t.mem_free=Math.round(t.mem.free/t.mem.total*100),t.disk=e.data.disk.slice(0,5),t.user=e.data.user.slice(0,7)})}}},r={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{directives:[{name:"loading",rawName:"v-loading.body",value:t.listLoading,expression:"listLoading",modifiers:{body:!0}}],staticClass:"dashboard-container"},[a("el-row",{attrs:{gutter:10}},[a("el-col",{attrs:{xs:16,sm:16,lg:8}},[a("el-card",{staticClass:"box-card-component"},[a("div",[a("span",{staticClass:"card-title"},[t._v("System Info")])]),t._v(" "),a("div",{staticStyle:{"margin-top":"30px"}},t._l(t.sys,function(e,s){return a("div",{staticClass:"list-item"},[a("span",[t._v(t._s(s))]),t._v(" "),a("span",{staticClass:"des"},[t._v(t._s(e))])])}))])],1),t._v(" "),a("el-col",{attrs:{xs:16,sm:16,lg:8}},[a("el-card",{staticClass:"box-card-component"},[a("div",[a("span",{staticClass:"card-title"},[t._v("CPU Status")])]),t._v(" "),a("div",{staticStyle:{"margin-top":"30px"}},t._l(t.cpu,function(e,s){return a("div",{staticClass:"progress-item"},[a("span",[t._v(t._s(s))]),t._v(" "),a("el-progress",{attrs:{percentage:e}})],1)}))])],1),t._v(" "),a("el-col",{attrs:{xs:16,sm:16,lg:8}},[a("el-card",{staticClass:"box-card-component"},[a("div",[a("span",{staticClass:"card-title"},[t._v("Memery Status")])]),t._v(" "),a("div",{staticStyle:{"margin-top":"30px"}},[a("div",{staticClass:"progress-item"},[a("span",[t._v("Total("+t._s(t._f("sizeformat")(t.mem.total))+"G)")]),t._v(" "),a("el-progress",{attrs:{percentage:100}})],1),t._v(" "),a("div",{staticClass:"progress-item"},[a("span",[t._v("Avaliable("+t._s(t._f("sizeformat")(t.mem.available))+"G)")]),t._v(" "),a("el-progress",{attrs:{percentage:t.mem_avaliable}})],1),t._v(" "),a("div",{staticClass:"progress-item"},[a("span",[t._v("Used(exclude cache & buffers "+t._s(t._f("sizeformat")(t.mem.total-t.mem.available))+"G)")]),t._v(" "),a("el-progress",{attrs:{percentage:t.mem.percent}})],1),t._v(" "),a("div",{staticClass:"progress-item"},[a("span",[t._v("Used(include cache & buffers "+t._s(t._f("sizeformat")(t.mem.used))+"G)")]),t._v(" "),a("el-progress",{attrs:{percentage:t.mem_used}})],1),t._v(" "),a("div",{staticClass:"progress-item"},[a("span",[t._v("Free("+t._s(t._f("sizeformat")(t.mem.free))+"G)")]),t._v(" "),a("el-progress",{attrs:{percentage:t.mem_free}})],1)])])],1)],1),t._v(" "),a("el-row",{attrs:{gutter:10}},[a("el-col",{attrs:{xs:32,sm:32,lg:16}},[a("el-card",{staticClass:"disk-card"},[a("div",[a("span",{staticClass:"card-title"},[t._v("Disk Info")])]),t._v(" "),a("el-table",{staticStyle:{width:"100%","padding-top":"15px"},attrs:{data:t.disk}},[a("el-table-column",{attrs:{label:"Device",width:"150","show-overflow-tooltip":"",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v("\n            "+t._s(e.row.device)+"\n          ")]}}])}),t._v(" "),a("el-table-column",{attrs:{label:"Mountpoint"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v("\n            "+t._s(e.row.mountpoint)+"\n          ")]}}])}),t._v(" "),a("el-table-column",{attrs:{label:"Space",width:"140",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v("\n            "+t._s(t._f("sizeformat")(e.row.space_total))+"G\n          ")]}}])}),t._v(" "),a("el-table-column",{attrs:{label:"Space Free",width:"140",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v("\n            "+t._s(t._f("sizeformat")(e.row.space_free))+"G\n          ")]}}])}),t._v(" "),a("el-table-column",{attrs:{label:"Space Used",width:"140",align:"center"},scopedSlots:t._u([{key:"default",fn:function(t){return[a("el-progress",{attrs:{percentage:t.row.space_used_percent,"show-text":!1}})]}}])}),t._v(" "),a("el-table-column",{attrs:{label:"Type",width:"100",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-tag",[t._v(" "+t._s(e.row.type))])]}}])})],1)],1)],1),t._v(" "),a("el-col",{attrs:{xs:16,sm:16,lg:8}},[a("el-card",{staticClass:"disk-card"},[a("div",[a("span",{staticClass:"card-title"},[t._v("User Info")])]),t._v(" "),a("el-table",{staticStyle:{width:"100%","padding-top":"15px"},attrs:{data:t.user}},[a("el-table-column",{attrs:{label:"Name",width:"150","show-overflow-tooltip":"",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v("\n            "+t._s(e.row.name)+"\n          ")]}}])}),t._v(" "),a("el-table-column",{attrs:{label:"Session Started"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v("\n            "+t._s(e.row.started)+"\n          ")]}}])}),t._v(" "),a("el-table-column",{attrs:{label:"Host",width:"100",align:"center"},scopedSlots:t._u([{key:"default",fn:function(e){return[t._v("\n            "+t._s(e.row.host)+"\n          ")]}}])})],1)],1)],1)],1)],1)},staticRenderFns:[]};var l=a("VU/8")(n,r,!1,function(t){a("SrHk")},"data-v-109aaa95",null);e.default=l.exports},SrHk:function(t,e,a){var s=a("yMm1");"string"==typeof s&&(s=[[t.i,s,""]]),s.locals&&(t.exports=s.locals);a("rjj0")("bf48a7cc",s,!0)},yMm1:function(t,e,a){(t.exports=a("FZ+f")(!1)).push([t.i,"\n.dashboard-container[data-v-109aaa95] {\n  margin: 30px;\n}\n.dashboard-text[data-v-109aaa95] {\n  font-size: 30px;\n  line-height: 46px;\n}\n.progress-item[data-v-109aaa95] {\n  margin-bottom: 10px;\n  font-size: 14px;\n}\n.list-item[data-v-109aaa95] {\n  line-height: 25px;\n}\n.des[data-v-109aaa95] {\n  float: right;\n}\n.box-card-component[data-v-109aaa95] {\n  height: 300px;\n  margin-top: 10px;\n}\n.disk-card[data-v-109aaa95] {\n  margin-top: 10px;\n  height: 500px;\n}\n.card-title[data-v-109aaa95] {\n  font-weight: bold;\n}\n",""])}});