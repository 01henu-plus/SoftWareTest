/**
 * Web登录功能自动化测试脚本
 * 课程：软件测试作业
 * 日期：2025年10月31日
 * 
 * 测试框架：原生JavaScript（可在浏览器控制台运行）
 * 说明：此脚本用于自动化测试login.html页面的登录功能
 */

class LoginTestSuite {
    constructor() {
        this.testResults = [];
        this.passCount = 0;
        this.failCount = 0;
        this.totalCount = 0;
    }

    // 初始化测试环境
    init() {
        console.log('='.repeat(80));
        console.log('Web登录功能自动化测试'.padStart(50));
        console.log('='.repeat(80));
        console.log(`测试开始时间: ${new Date().toLocaleString('zh-CN')}`);
        console.log('='.repeat(80));
        console.log('');
    }

    // 等待函数
    async wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // 获取DOM元素
    getElements() {
        return {
            usernameInput: document.getElementById('username'),
            passwordInput: document.getElementById('password'),
            loginButton: document.getElementById('loginButton'),
            messageBox: document.getElementById('messageBox'),
            usernameError: document.getElementById('usernameError'),
            passwordError: document.getElementById('passwordError')
        };
    }

    // 清空输入框
    clearInputs() {
        const elements = this.getElements();
        elements.usernameInput.value = '';
        elements.passwordInput.value = '';
        elements.usernameInput.classList.remove('error');
        elements.passwordInput.classList.remove('error');
        elements.messageBox.style.display = 'none';
    }

    // 输入用户名和密码
    async inputCredentials(username, password) {
        const elements = this.getElements();
        
        elements.usernameInput.value = username;
        elements.usernameInput.dispatchEvent(new Event('input', { bubbles: true }));
        await this.wait(100);
        
        elements.passwordInput.value = password;
        elements.passwordInput.dispatchEvent(new Event('input', { bubbles: true }));
        await this.wait(100);
    }

    // 点击登录按钮
    async clickLogin() {
        const elements = this.getElements();
        elements.loginButton.click();
        await this.wait(1500); // 等待登录处理完成
    }

    // 记录测试结果
    logResult(testId, testName, input, expected, actual, status) {
        this.totalCount++;
        const result = {
            testId,
            testName,
            input,
            expected,
            actual,
            status,
            timestamp: new Date().toISOString()
        };
        
        this.testResults.push(result);
        
        if (status === 'PASS') {
            this.passCount++;
            console.log(`✓ ${testId} - ${testName}: PASS`);
        } else {
            this.failCount++;
            console.log(`✗ ${testId} - ${testName}: FAIL`);
        }
        
        console.log(`  输入: ${JSON.stringify(input)}`);
        console.log(`  期望: ${expected}`);
        console.log(`  实际: ${actual}`);
        console.log('');
    }

    // 测试用例1：空用户名
    async testCase01() {
        console.log('【TC001】测试空用户名');
        this.clearInputs();
        await this.inputCredentials('', '123456');
        await this.clickLogin();
        
        const elements = this.getElements();
        const hasError = elements.usernameError.classList.contains('show');
        const errorMsg = elements.usernameError.textContent;
        
        this.logResult(
            'TC001',
            '空用户名验证',
            { username: '', password: '123456' },
            '显示"用户名不能为空"错误',
            hasError ? errorMsg : '无错误提示',
            hasError && errorMsg.includes('不能为空') ? 'PASS' : 'FAIL'
        );
    }

    // 测试用例2：空密码
    async testCase02() {
        console.log('【TC002】测试空密码');
        this.clearInputs();
        await this.inputCredentials('admin', '');
        await this.clickLogin();
        
        const elements = this.getElements();
        const hasError = elements.passwordError.classList.contains('show');
        const errorMsg = elements.passwordError.textContent;
        
        this.logResult(
            'TC002',
            '空密码验证',
            { username: 'admin', password: '' },
            '显示"密码不能为空"错误',
            hasError ? errorMsg : '无错误提示',
            hasError && errorMsg.includes('不能为空') ? 'PASS' : 'FAIL'
        );
    }

    // 测试用例3：用户名过短
    async testCase03() {
        console.log('【TC003】测试用户名过短');
        this.clearInputs();
        await this.inputCredentials('ab', '123456');
        await this.clickLogin();
        
        const elements = this.getElements();
        const hasError = elements.usernameError.classList.contains('show');
        const errorMsg = elements.usernameError.textContent;
        
        this.logResult(
            'TC003',
            '用户名长度验证（过短）',
            { username: 'ab', password: '123456' },
            '显示"用户名长度至少3个字符"错误',
            hasError ? errorMsg : '无错误提示',
            hasError && errorMsg.includes('至少3个字符') ? 'PASS' : 'FAIL'
        );
    }

    // 测试用例4：密码过短
    async testCase04() {
        console.log('【TC004】测试密码过短');
        this.clearInputs();
        await this.inputCredentials('admin', '12345');
        await this.clickLogin();
        
        const elements = this.getElements();
        const hasError = elements.passwordError.classList.contains('show');
        const errorMsg = elements.passwordError.textContent;
        
        this.logResult(
            'TC004',
            '密码长度验证（过短）',
            { username: 'admin', password: '12345' },
            '显示"密码长度至少6个字符"错误',
            hasError ? errorMsg : '无错误提示',
            hasError && errorMsg.includes('至少6个字符') ? 'PASS' : 'FAIL'
        );
    }

    // 测试用例5：用户名包含特殊字符
    async testCase05() {
        console.log('【TC005】测试用户名包含特殊字符');
        this.clearInputs();
        await this.inputCredentials('admin@123', '123456');
        await this.clickLogin();
        
        const elements = this.getElements();
        const hasError = elements.usernameError.classList.contains('show');
        const errorMsg = elements.usernameError.textContent;
        
        this.logResult(
            'TC005',
            '用户名格式验证（特殊字符）',
            { username: 'admin@123', password: '123456' },
            '显示"用户名只能包含字母、数字和下划线"错误',
            hasError ? errorMsg : '无错误提示',
            hasError && errorMsg.includes('字母、数字和下划线') ? 'PASS' : 'FAIL'
        );
    }

    // 测试用例6：正确的用户名和密码
    async testCase06() {
        console.log('【TC006】测试正确的用户名和密码');
        this.clearInputs();
        await this.inputCredentials('admin', '123456');
        await this.clickLogin();
        
        const elements = this.getElements();
        const messageText = elements.messageBox.textContent;
        const isSuccess = elements.messageBox.classList.contains('success');
        
        this.logResult(
            'TC006',
            '正确凭证登录',
            { username: 'admin', password: '123456' },
            '登录成功',
            isSuccess ? '登录成功' : messageText,
            isSuccess ? 'PASS' : 'FAIL'
        );
    }

    // 测试用例7：错误的用户名
    async testCase07() {
        console.log('【TC007】测试错误的用户名');
        this.clearInputs();
        await this.inputCredentials('wronguser', '123456');
        await this.clickLogin();
        
        const elements = this.getElements();
        const messageText = elements.messageBox.textContent;
        const isError = elements.messageBox.classList.contains('error');
        
        this.logResult(
            'TC007',
            '错误用户名登录',
            { username: 'wronguser', password: '123456' },
            '登录失败，显示错误信息',
            isError ? messageText : '无错误提示',
            isError && messageText.includes('错误') ? 'PASS' : 'FAIL'
        );
    }

    // 测试用例8：错误的密码
    async testCase08() {
        console.log('【TC008】测试错误的密码');
        this.clearInputs();
        await this.inputCredentials('admin', 'wrongpass');
        await this.clickLogin();
        
        const elements = this.getElements();
        const messageText = elements.messageBox.textContent;
        const isError = elements.messageBox.classList.contains('error');
        
        this.logResult(
            'TC008',
            '错误密码登录',
            { username: 'admin', password: 'wrongpass' },
            '登录失败，显示错误信息',
            isError ? messageText : '无错误提示',
            isError && messageText.includes('错误') ? 'PASS' : 'FAIL'
        );
    }

    // 测试用例9：testuser账户登录
    async testCase09() {
        console.log('【TC009】测试testuser账户登录');
        this.clearInputs();
        await this.inputCredentials('testuser', 'password123');
        await this.clickLogin();
        
        const elements = this.getElements();
        const messageText = elements.messageBox.textContent;
        const isSuccess = elements.messageBox.classList.contains('success');
        
        this.logResult(
            'TC009',
            'testuser账户登录',
            { username: 'testuser', password: 'password123' },
            '登录成功',
            isSuccess ? '登录成功' : messageText,
            isSuccess ? 'PASS' : 'FAIL'
        );
    }

    // 测试用例10：用户名过长
    async testCase10() {
        console.log('【TC010】测试用户名过长');
        this.clearInputs();
        const longUsername = 'a'.repeat(25);
        await this.inputCredentials(longUsername, '123456');
        await this.clickLogin();
        
        const elements = this.getElements();
        const hasError = elements.usernameError.classList.contains('show');
        const errorMsg = elements.usernameError.textContent;
        
        this.logResult(
            'TC010',
            '用户名长度验证（过长）',
            { username: longUsername, password: '123456' },
            '显示"用户名长度不能超过20个字符"错误',
            hasError ? errorMsg : '无错误提示',
            hasError && errorMsg.includes('不能超过20个字符') ? 'PASS' : 'FAIL'
        );
    }

    // 运行所有测试
    async runAllTests() {
        this.init();
        
        await this.testCase01();
        await this.testCase02();
        await this.testCase03();
        await this.testCase04();
        await this.testCase05();
        await this.testCase06();
        await this.testCase07();
        await this.testCase08();
        await this.testCase09();
        await this.testCase10();
        
        this.generateReport();
    }

    // 生成测试报告
    generateReport() {
        console.log('='.repeat(80));
        console.log('测试执行总结'.padStart(50));
        console.log('='.repeat(80));
        console.log(`测试结束时间: ${new Date().toLocaleString('zh-CN')}`);
        console.log(`总测试用例数: ${this.totalCount}`);
        console.log(`通过: ${this.passCount} (${(this.passCount/this.totalCount*100).toFixed(1)}%)`);
        console.log(`失败: ${this.failCount} (${(this.failCount/this.totalCount*100).toFixed(1)}%)`);
        console.log('='.repeat(80));
        
        // 生成详细报告表格
        console.log('\n测试结果详情:');
        console.table(this.testResults);
        
        // 保存结果到localStorage
        localStorage.setItem('loginTestResults', JSON.stringify({
            summary: {
                total: this.totalCount,
                pass: this.passCount,
                fail: this.failCount,
                passRate: (this.passCount/this.totalCount*100).toFixed(1) + '%'
            },
            details: this.testResults,
            timestamp: new Date().toISOString()
        }));
        
        console.log('\n测试报告已保存到 localStorage.loginTestResults');
        console.log('可以使用以下命令查看: localStorage.getItem("loginTestResults")');
    }
}

// 使用说明
console.log(`
╔════════════════════════════════════════════════════════════════════════╗
║                    Web登录功能自动化测试脚本                           ║
║                    软件测试作业 - VSCode环境                           ║
╚════════════════════════════════════════════════════════════════════════╝

使用方法：
1. 在VSCode中打开 login.html 文件
2. 使用Live Server或其他方式在浏览器中打开页面
3. 打开浏览器开发者工具（F12）
4. 在控制台中运行以下命令启动测试：

   const testSuite = new LoginTestSuite();
   testSuite.runAllTests();

5. 测试完成后，查看控制台输出的测试报告

注意：测试过程中请勿手动操作页面
`);

// 导出测试套件（如果在模块环境中）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LoginTestSuite;
}
