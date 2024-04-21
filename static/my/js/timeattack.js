var timeattackchart = echarts.init(document.getElementById('timeattack'));

// 指定图表的配置项和数据
timeattackoption = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            lineStyle: {
                color: '#0088d4'
            }
        }
    },
    legend: {
        icon: 'rect',
        itemWidth: 14,
        itemHeight: 5,
        itemGap: 13,
        data: ['攻击数量(万次)'],
        right: '4%',
        textStyle: {
            fontSize: 12,
            color: '#F1F1F3'
        }
    },
    grid: {
        top: '10%',
        left: '5%',
        right: '2%',
        bottom: '20%',
        containLabel: false
    },
    xAxis: [{
        type: 'category',
        boundaryGap: false,
        axisLine: {
            lineStyle: {
                color: '#57617B'
            }
        },
        splitLine: {
            show: true,
            lineStyle: {
                // color: ['red', 'blue'],
                color: '#57617B',
                type: 'dashed'
            }
        },
        data: ['8:00','10:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', '13:50', '13:55']
    }],
    yAxis: [{
        type: 'value',
        name: '次数（万次）',
        axisTick: {
            show: false
        },
        axisLine: {
            lineStyle: {
                color: '#57617B',
            }
        },
        axisLabel: {
            margin: 10,
            textStyle: {
                fontSize: 14
            }
        },
        splitLine: {
            // show:false,
            lineStyle: {
                color: '#57617B',
                type:'dashed'
            }
        }
    }],
    series: [

        {
            name: '攻击数量(次)',
            type: 'line',
            // smooth: false,
            smooth: true,//曲线是否平滑显示
            symbol: 'circle',
            symbolSize: 5,
            showSymbol: false,
            lineStyle: {
                normal: {
                    width: 1,
                    // color:'red'
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgba(0, 136, 212, 0.3)'
                    }, {
                        offset: 0.8,
                        color: 'rgba(0, 136, 212, 0)'
                    }], false),
                    shadowColor: 'rgba(0, 0, 0, 0.1)',
                    shadowBlur: 10
                }
            },
            itemStyle: {
                normal: {
                    color: 'rgb(0,136,212)',
                    borderColor: 'rgba(0,136,212,0.2)',
                    borderWidth: 12

                }
            },
            <!-- data: [5000, 10000, 23000, 14500, 32200, 26500, 42200, 22000, 28000, 35000, 25000, 16000] -->
            data: [5000, 10000, 23000, 14500, 32200, 26500, 42200, 22000, 28000, 35000, 25000, 16000]
        },]

};
timeattackchart.setOption(timeattackoption);
$.get("/attack/time", function (data) {
    out = data.result;
    timeattackoption.xAxis[0].data.splice(0, timeattackoption.xAxis[0].data.length);
    timeattackoption.series[0].data.splice(0, timeattackoption.series[0].data.length);
    for (var i = 0; i < 20; i++) {
        timeattackoption.xAxis[0].data.push(out[i][0]);
        timeattackoption.series[0].data.push(out[i][1]);
    }
    timeattackchart.setOption(timeattackoption);
});
