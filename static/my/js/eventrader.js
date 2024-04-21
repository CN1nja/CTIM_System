// 基于准备好的dom，初始化echarts实例
var eventraderchart = echarts.init(document.getElementById('eventrader'));

// 指定图表的配置项和数据
// Schema:
// AQIindex,PM2.5,PM10,CO,NO2,SO2，递增序号（可以省略）
var dataBJ = [
    [0, 0, 0],
];

var lineStyle = {
    normal: {
        width: 1,
        opacity: 0.5
    }
};

raderoption = {
    legend: {
        left: 0,
        // right:0,
        // bottom: -10,
        orient: 'vertical',
        data: [],
        itemGap: 10,
        itemWidth: 15,
        itemHeight: 8,
        textStyle: {
            color: '#fff',
            fontSize: 2
        },
        selectedMode: 'single'
    },
    tooltip: { // 提示框组件
        // show:false,
        show: true,
        trigger: 'item', // 触发类型 可选为：'axis' | 'item' | 'none'
        axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow', // 默认为直线，可选为：'line' | 'shadow'
            shadowStyle: {
                // color: defaultShadowColor
            }
        }
    },
    radar: {
        indicator: [
            {name: '低危', max: 300},
            {name: '中危', max: 250},
            {name: '高危', max: 300},

        ],
        radius: '70%',
        shape: 'circle',
        splitNumber: 3,//指示器轴的分割段数，
        name: {
            textStyle: {
                color: 'rgb(238, 197, 102)',
                fontSize: 5
            }
        },
        splitLine: {
            lineStyle: {//指示器轴的分割段数的颜色，就是一圈一圈的颜色
                color: [
                    'rgba(238, 197, 102, 0.1)', 'rgba(238, 197, 102, 0.2)',
                    'rgba(238, 197, 102, 0.4)', 'rgba(238, 197, 102, 0.6)',
                    'rgba(238, 197, 102, 0.8)', 'rgba(238, 197, 102, 1)'
                ].reverse()
            }
        },
        splitArea: {
            show: false
        },
        axisLine: {
            lineStyle: {
                color: 'rgba(238, 197, 102, 0.5)'
            }
        }
    },

    series: [
        {
            name: '事件',
            type: 'radar',
            lineStyle: lineStyle,

            // data: [{value:[33,45,67,2,34,56],name:'北京'}],
            data: dataBJ,
            symbol: 'circle',
            itemStyle: {
                normal: {
                    color: '#F9713C'
                }
            },
            areaStyle: {
                normal: {
                    opacity: 0.1
                }
            }
        }

    ]
};

$.get("/event_radar", function (data) {

    for (var j = 0; j < data.result.length; j++) {

        if (data.result[j][0] == "低危") {
            dataBJ[0][0] = data.result[j][1];
        }
        if (data.result[j][0] == "中危") {
            dataBJ[0][1] = data.result[j][1];
        }
        if (data.result[j][0] == "高危") {
            dataBJ[0][2] = data.result[j][1];
        }

    }
    eventraderchart.setOption(raderoption);
});

