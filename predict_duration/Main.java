import java.util.Scanner;

public class Main {
    public static int MAX = 100;
    public static int n;
    public static int[][] value = new int[MAX][MAX];   //给定二分图的权重值
    public static int[] lx = new int[MAX];   //记录二分图左半部分顶点的可行顶标
    public static int[] ly = new int[MAX];   //记录二分图右半部分顶点的可行顶标
    public static boolean[] sx = new boolean[MAX];//用于记录二分图左半部分顶点是否在最终结果中
    public static boolean[] sy = new boolean[MAX];//用于记录二分图右半部分顶点是否在最终结果中
    public static int[] pre = new int[MAX];  //用于记录最终结果中顶点y匹配的顶点x

    public boolean dfs(int x) {   //采用匈牙利算法找增广路径
        sx[x] = true;       //代表左半部分顶点x包含在最终结果中
        for(int y = 0;y < n;y++) {
            if(!sy[y] && lx[x] + ly[y] == value[x][y]) {
                sy[y] = true;   //代表右半部分顶点y包含在最终结果中
                if(pre[y] == -1 || dfs(pre[y])) {
                    pre[y] = x;
                    return true;
                }
            }
        }
        return false;
    }

    public int getKM(int judge) {
        if(judge == -1) {  //代表寻找二分图的最小权匹配
            for(int i = 0;i < n;i++)
                for(int j = 0;j < n;j++)
                    value[i][j] = -1 * value[i][j];  //把权值变为相反数，相当于找最大权匹配
        }
        //初始化lx[i]和ly[i]
        for(int i = 0;i < n;i++) {
            ly[i] = 0;
            lx[i] = Integer.MIN_VALUE;
            for(int j = 0;j < n;j++) {
                if(value[i][j] > lx[i])
                    lx[i] = value[i][j];
            }
        }

        for(int i = 0;i < n;i++)
            pre[i] = -1;      //初始化右半部分顶点y的匹配顶点为-1

        for(int x = 0;x < n;x++) { //从左半部分顶点开始，寻找二分图完美匹配的相等子图完美匹配
            while(true) {
                for(int i = 0;i < n;i++) {//每次寻找x的增广路径，初始化sx[i]和sy[i]均为被遍历
                    sx[i] = false;
                    sy[i] = false;
                }
                if(dfs(x))  //找到从x出发的增广路径，结束循环，寻找下一个x的增广路径
                    break;
                //下面对于没有找到顶点x的增广路径进行lx[i]和ly[i]值的调整
                int min = Integer.MAX_VALUE;
                for(int i = 0;i < n;i++) {
                    if(sx[i]) {  //当sx[i]已被遍历时
                        for(int j = 0;j < n;j++) {
                            if(!sy[j]) {  //当sy[j]未被遍历时
                                if(lx[i] + ly[j] - value[i][j] < min)
                                    min = lx[i] + ly[j] - value[i][j];
                            }
                        }
                    }
                }
                if(min == 0)
                    return -1;
                for(int i = 0;i < n;i++) {
                    if(sx[i])
                        lx[i] = lx[i] - min;
                    if(sy[i])
                        ly[i] = ly[i] + min;
                }
            }
        }

        int sum = 0;
        for(int y = 0;y < n;y++) {
            System.out.println("y顶点"+y+"和x顶点"+pre[y]+"匹配");
            if(pre[y] != -1)
                sum = sum + value[pre[y]][y];
        }
        if(judge == -1)
            sum = -1 * sum;
        return sum;
    }

    public static void main(String[] args) {
        Main test = new Main();
        Scanner in = new Scanner(System.in);
        n = in.nextInt();
        int k = in.nextInt();   //给定二分图的有向边数目
        for(int i = 0;i < k;i++) {
            int x = in.nextInt();
            int y = in.nextInt();
            int v = in.nextInt();
            value[x][y] = v;
        }
        System.out.println(test.getKM(1));
    }
}