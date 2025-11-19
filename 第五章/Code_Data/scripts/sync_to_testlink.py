#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TestLink 集成脚本
功能：将自动化测试结果同步到 TestLink 测试管理平台
使用方法：python sync_to_testlink.py --results all-test-results.xml
"""

import argparse
import xml.etree.ElementTree as ET
import os
import sys
from typing import Dict, List

try:
    import testlink
except ImportError:
    print("警告: testlink 模块未安装。请运行: pip install TestLink-API-Python-client")
    testlink = None


class TestLinkSync:
    """TestLink 同步工具类"""
    
    def __init__(self, server_url: str, api_key: str, project_name: str, test_plan_name: str):
        """
        初始化 TestLink 连接
        
        Args:
            server_url: TestLink 服务器地址，如 http://testlink.example.com/lib/api/xmlrpc/v1/xmlrpc.php
            api_key: TestLink API Key
            project_name: 项目名称
            test_plan_name: 测试计划名称
        """
        self.server_url = server_url
        self.api_key = api_key
        self.project_name = project_name
        self.test_plan_name = test_plan_name
        self.tl_client = None
        
        if testlink:
            try:
                self.tl_client = testlink.TestlinkAPIClient(server_url, api_key)
                print(f"✓ 已连接到 TestLink: {server_url}")
            except Exception as e:
                print(f"✗ 连接 TestLink 失败: {e}")
    
    def parse_junit_results(self, xml_file: str) -> List[Dict]:
        """
        解析 JUnit XML 测试结果
        
        Args:
            xml_file: JUnit XML 文件路径
            
        Returns:
            测试用例结果列表
        """
        if not os.path.exists(xml_file):
            print(f"✗ 文件不存在: {xml_file}")
            return []
        
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        results = []
        for testcase in root.iter('testcase'):
            test_name = testcase.get('name')
            test_class = testcase.get('classname', '')
            time = float(testcase.get('time', 0))
            
            status = 'p'  # passed
            notes = f"执行时间: {time:.2f}秒"
            
            # 检查是否失败
            failure = testcase.find('failure')
            if failure is not None:
                status = 'f'  # failed
                notes += f"\n失败原因: {failure.get('message', '')}\n{failure.text or ''}"
            
            # 检查是否跳过
            skipped = testcase.find('skipped')
            if skipped is not None:
                status = 'b'  # blocked
                notes += f"\n跳过原因: {skipped.get('message', '')}"
            
            # 检查是否错误
            error = testcase.find('error')
            if error is not None:
                status = 'f'
                notes += f"\n错误信息: {error.get('message', '')}\n{error.text or ''}"
            
            results.append({
                'name': test_name,
                'class': test_class,
                'status': status,
                'notes': notes,
                'execution_time': time
            })
        
        return results
    
    def sync_results(self, results: List[Dict]) -> bool:
        """
        将测试结果同步到 TestLink
        
        Args:
            results: 测试结果列表
            
        Returns:
            是否成功
        """
        if not self.tl_client:
            print("⚠ TestLink 客户端未初始化，跳过同步")
            return False
        
        try:
            # 获取项目 ID
            projects = self.tl_client.getProjects()
            project_id = None
            for proj in projects:
                if proj['name'] == self.project_name:
                    project_id = proj['id']
                    break
            
            if not project_id:
                print(f"✗ 找不到项目: {self.project_name}")
                return False
            
            # 获取测试计划 ID
            test_plans = self.tl_client.getProjectTestPlans(project_id)
            test_plan_id = None
            for plan in test_plans:
                if plan['name'] == self.test_plan_name:
                    test_plan_id = plan['id']
                    break
            
            if not test_plan_id:
                print(f"✗ 找不到测试计划: {self.test_plan_name}")
                return False
            
            # 同步每个测试结果
            success_count = 0
            for result in results:
                try:
                    # 根据测试名称查找 TestLink 中的测试用例
                    # 注意：这里假设测试用例的外部 ID 或名称与自动化测试名称匹配
                    test_case = self.find_test_case_by_name(project_id, result['name'])
                    
                    if test_case:
                        # 报告执行结果
                        self.tl_client.reportTCResult(
                            testcaseid=test_case['id'],
                            testplanid=test_plan_id,
                            status=result['status'],
                            notes=result['notes']
                        )
                        print(f"✓ 已同步: {result['name']} - {self.get_status_name(result['status'])}")
                        success_count += 1
                    else:
                        print(f"⚠ 未找到测试用例: {result['name']}")
                
                except Exception as e:
                    print(f"✗ 同步失败 {result['name']}: {e}")
            
            print(f"\n同步完成: {success_count}/{len(results)} 个测试用例")
            return True
        
        except Exception as e:
            print(f"✗ 同步过程出错: {e}")
            return False
    
    def find_test_case_by_name(self, project_id: str, test_name: str):
        """根据名称查找测试用例（简化版）"""
        # 实际实现中需要遍历测试套件并匹配名称
        # 这里仅作示例
        try:
            test_cases = self.tl_client.getTestCasesForTestSuite(project_id, deep=True)
            for tc in test_cases:
                if tc.get('name') == test_name or tc.get('external_id') == test_name:
                    return tc
        except:
            pass
        return None
    
    @staticmethod
    def get_status_name(status: str) -> str:
        """获取状态名称"""
        status_map = {
            'p': '通过',
            'f': '失败',
            'b': '阻塞',
            'n': '未执行'
        }
        return status_map.get(status, '未知')


def main():
    parser = argparse.ArgumentParser(description='同步测试结果到 TestLink')
    parser.add_argument('--results', required=True, help='JUnit XML 测试结果文件路径')
    parser.add_argument('--server', default=os.getenv('TESTLINK_URL', 'http://testlink.example.com/lib/api/xmlrpc/v1/xmlrpc.php'), 
                       help='TestLink 服务器 API 地址')
    parser.add_argument('--api-key', default=os.getenv('TESTLINK_API_KEY', ''), 
                       help='TestLink API Key')
    parser.add_argument('--project', default=os.getenv('TESTLINK_PROJECT', '电商平台'), 
                       help='项目名称')
    parser.add_argument('--test-plan', default=os.getenv('TESTLINK_TEST_PLAN', '登录模块测试计划'), 
                       help='测试计划名称')
    
    args = parser.parse_args()
    
    # 检查 API Key
    if not args.api_key:
        print("⚠ 未配置 TestLink API Key")
        print("请设置环境变量 TESTLINK_API_KEY 或使用 --api-key 参数")
        print("\n演示模式：仅解析测试结果，不实际同步")
    
    # 创建同步工具
    syncer = TestLinkSync(args.server, args.api_key, args.project, args.test_plan)
    
    # 解析测试结果
    print(f"\n解析测试结果: {args.results}")
    results = syncer.parse_junit_results(args.results)
    
    if not results:
        print("✗ 没有找到测试结果")
        sys.exit(1)
    
    print(f"\n找到 {len(results)} 个测试用例:")
    for r in results:
        status_name = syncer.get_status_name(r['status'])
        print(f"  - {r['name']}: {status_name}")
    
    # 同步到 TestLink
    if args.api_key:
        print("\n开始同步到 TestLink...")
        success = syncer.sync_results(results)
        sys.exit(0 if success else 1)
    else:
        print("\n提示: 配置 TestLink API Key 后可自动同步结果")
        sys.exit(0)


if __name__ == '__main__':
    main()
