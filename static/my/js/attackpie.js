// 基于准备好的dom，初始化echarts实例
var attackpiechart = echarts.init(document.getElementById('attackpie'));

pieoption = {
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    series: [
        {
            name: '攻击次数',
            type: 'pie',
            radius: '65%',
            center: ['35%', '50%'],
            data: [],
            // roseType: 'radius',
            itemStyle: {
                normal: {
                    color: '#1e9f99',
                    shadowBlur: 500,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                },
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};

currentIndex = -1;

setInterval(function () {
    var dataLen = pieoption.series[0].data.length;
    // 取消之前高亮的图形
    attackpiechart.dispatchAction({
        type: 'downplay',
        seriesIndex: 0,
        dataIndex: currentIndex
    });
    currentIndex = (currentIndex + 1) % dataLen;
    // 高亮当前图形
    attackpiechart.dispatchAction({
        type: 'highlight',
        seriesIndex: 0,
        dataIndex: currentIndex
    });
    // 显示 tooltip
    attackpiechart.dispatchAction({
        type: 'showTip',
        seriesIndex: 0,
        dataIndex: currentIndex
    });
}, 1000);

$.get("/attack/time", function (data) {
    out = data.result;
    for (var i = 0; i < 12; i++) {
        pieoption.series[0].data.push({value: out[i][1], name: out[i][0]});
    }
    attackpiechart.setOption(pieoption)
});

