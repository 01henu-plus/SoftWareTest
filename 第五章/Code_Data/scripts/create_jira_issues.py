#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Jira 集成脚本
功能：为失败的测试用例自动创建 Jira 缺陷
使用方法：python create_jira_issues.py --results all-test-results.xml
"""

import argparse
import xml.etree.ElementTree as ET
import os
import sys
from typing import Dict, List
from datetime import datetime

try:
    from jira import JIRA
except ImportError:
    print("警告: jira 模块未安装。请运行: pip install jira")
    JIRA = None


class JiraIntegration:
    """Jira 集成工具类"""
    
    def __init__(self, server: str, email: str, api_token: str, project_key: str):
        """
        初始化 Jira 连接
        
        Args:
            server: Jira 服务器地址，如 https://your-domain.atlassian.net
            email: Jira 用户邮箱
            api_token: Jira API Token
            project_key: 项目 Key，如 PROJ
        """
        self.server = server
        self.email = email
        self.api_token = api_token
        self.project_key = project_key
        self.jira_client = None
        
        if JIRA:
            try:
                self.jira_client = JIRA(
                    server=server,
                    basic_auth=(email, api_token)
                )
                print(f"✓ 已连接到 Jira: {server}")
            except Exception as e:
                print(f"✗ 连接 Jira 失败: {e}")
    
    def parse_junit_failures(self, xml_file: str) -> List[Dict]:
        """
        解析 JUnit XML 中的失败测试
        
        Args:
            xml_file: JUnit XML 文件路径
            
        Returns:
            失败的测试用例列表
        """
        if not os.path.exists(xml_file):
            print(f"✗ 文件不存在: {xml_file}")
            return []
        
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        failures = []
        for testcase in root.iter('testcase'):
            test_name = testcase.get('name')
            test_class = testcase.get('classname', '')
            time = float(testcase.get('time', 0))
            
            # 检查失败或错误
            failure = testcase.find('failure')
            error = testcase.find('error')
            
            if failure is not None or error is not None:
                issue_elem = failure if failure is not None else error
                message = issue_elem.get('message', '无详细信息')
                stacktrace = issue_elem.text or ''
                
                failures.append({
                    'name': test_name,
                    'class': test_class,
                    'message': message,
                    'stacktrace': stacktrace,
                    'execution_time': time
                })
        
        return failures
    
    def create_issue(self, test_failure: Dict, build_url: str = '') -> str:
        """
        为失败的测试创建 Jira Issue
        
        Args:
            test_failure: 测试失败信息
            build_url: Jenkins 构建 URL
            
        Returns:
            创建的 Issue Key，失败返回空字符串
        """
        if not self.jira_client:
            print("⚠ Jira 客户端未初始化，跳过创建")
            return ''
        
        try:
            # 检查是否已存在相同的 Issue（避免重复创建）
            existing = self.find_existing_issue(test_failure['name'])
            if existing:
                print(f"⚠ Issue 已存在: {existing.key} - {test_failure['name']}")
                # 可选：更新现有 Issue，添加评论
                self.add_comment_to_issue(existing.key, 
                    f"测试再次失败\n构建: {build_url}\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                return existing.key
            
            # 创建 Issue
            summary = f"[自动化测试] {test_failure['name']} 失败"
            
            description = f"""
h2. 测试失败详情

*测试用例:* {{{{color:red}}}}{test_failure['name']}{{{{color}}}}
*测试类:* {test_failure['class']}
*执行时间:* {test_failure['execution_time']:.2f} 秒
*失败信息:* {test_failure['message']}

h3. 堆栈跟踪
{{{{code}}}}
{test_failure['stacktrace'][:2000]}  
{{{{code}}}}

h3. 构建信息
*Jenkins 构建:* {build_url if build_url else '未提供'}
*失败时间:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

h3. 建议操作
# 检查测试日志和截图（如有）
# 在本地环境重现问题
# 修复代码或更新测试用例
# 重新运行测试验证修复
"""
            
            issue_dict = {
                'project': {'key': self.project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': 'Bug'},
                'priority': {'name': 'Medium'},
                'labels': ['automated-test', 'test-failure', 'login-module']
            }
            
            new_issue = self.jira_client.create_issue(fields=issue_dict)
            print(f"✓ 已创建 Issue: {new_issue.key} - {test_failure['name']}")
            return new_issue.key
        
        except Exception as e:
            print(f"✗ 创建 Issue 失败 {test_failure['name']}: {e}")
            return ''
    
    def find_existing_issue(self, test_name: str):
        """查找已存在的相同测试的 Issue"""
        try:
            # 搜索最近创建的、未关闭的、包含测试名称的 Issue
            jql = f'project = {self.project_key} AND summary ~ "{test_name}" AND status != Done AND status != Closed ORDER BY created DESC'
            issues = self.jira_client.search_issues(jql, maxResults=1)
            return issues[0] if issues else None
        except:
            return None
    
    def add_comment_to_issue(self, issue_key: str, comment: str):
        """为 Issue 添加评论"""
        try:
            self.jira_client.add_comment(issue_key, comment)
            print(f"✓ 已添加评论到 {issue_key}")
        except Exception as e:
            print(f"✗ 添加评论失败: {e}")
    
    def create_issues_for_failures(self, failures: List[Dict], build_url: str = '') -> List[str]:
        """
        为所有失败的测试创建 Issues
        
        Args:
            failures: 失败的测试列表
            build_url: Jenkins 构建 URL
            
        Returns:
            创建的 Issue Key 列表
        """
        if not self.jira_client:
            print("⚠ Jira 客户端未初始化，跳过创建")
            return []
        
        created_issues = []
        for failure in failures:
            issue_key = self.create_issue(failure, build_url)
            if issue_key:
                created_issues.append(issue_key)
        
        return created_issues


def main():
    parser = argparse.ArgumentParser(description='为失败的测试创建 Jira Issues')
    parser.add_argument('--results', required=True, help='JUnit XML 测试结果文件路径')
    parser.add_argument('--server', default=os.getenv('JIRA_SERVER', 'https://your-domain.atlassian.net'), 
                       help='Jira 服务器地址')
    parser.add_argument('--email', default=os.getenv('JIRA_EMAIL', ''), 
                       help='Jira 用户邮箱')
    parser.add_argument('--api-token', default=os.getenv('JIRA_API_TOKEN', ''), 
                       help='Jira API Token')
    parser.add_argument('--project', default=os.getenv('JIRA_PROJECT_KEY', 'PROJ'), 
                       help='Jira 项目 Key')
    parser.add_argument('--build-url', default=os.getenv('BUILD_URL', ''), 
                       help='Jenkins 构建 URL')
    
    args = parser.parse_args()
    
    # 检查必需的参数
    if not args.email or not args.api_token:
        print("⚠ 未配置 Jira 认证信息")
        print("请设置环境变量:")
        print("  - JIRA_EMAIL: Jira 用户邮箱")
        print("  - JIRA_API_TOKEN: Jira API Token")
        print("\n演示模式：仅解析失败的测试，不实际创建 Issues")
    
    # 创建 Jira 集成工具
    jira_tool = JiraIntegration(args.server, args.email, args.api_token, args.project)
    
    # 解析失败的测试
    print(f"\n解析测试结果: {args.results}")
    failures = jira_tool.parse_junit_failures(args.results)
    
    if not failures:
        print("✓ 所有测试都通过了！无需创建 Issues")
        sys.exit(0)
    
    print(f"\n找到 {len(failures)} 个失败的测试:")
    for f in failures:
        print(f"  - {f['name']}: {f['message'][:80]}...")
    
    # 创建 Jira Issues
    if args.email and args.api_token:
        print(f"\n开始为失败的测试创建 Jira Issues (项目: {args.project})...")
        created = jira_tool.create_issues_for_failures(failures, args.build_url)
        
        if created:
            print(f"\n成功创建 {len(created)} 个 Issues:")
            for issue_key in created:
                print(f"  - {args.server}/browse/{issue_key}")
        
        sys.exit(0 if created else 1)
    else:
        print("\n提示: 配置 Jira 认证信息后可自动创建 Issues")
        sys.exit(0)


if __name__ == '__main__':
    main()
